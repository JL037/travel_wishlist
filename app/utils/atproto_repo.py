"""PDS repo writes (com.atproto.repo.*) for Phase 2 dual-write.

Every authenticated call to a user's PDS needs a fresh DPoP proof bound to
that session's access token (RFC 9449, same requirement as the OAuth token
endpoint calls in app/utils/atproto_oauth.py) plus that access token itself
in the Authorization header (`DPoP <token>`, not `Bearer <token>`). The PDS
is a *separate* resource server from the authorization server the tokens
came from, so it has its own DPoP nonce - AtprotoSession tracks the two
(`dpop_authserver_nonce`, `dpop_pds_nonce`) separately for this reason.

NOTE ON VERIFICATION: like the rest of the AT Proto OAuth work in this repo,
this was written against the spec (atproto.com/specs/xrpc,
atproto.com/specs/oauth) without live network access to verify field names.
com.atproto.repo.createRecord/putRecord/deleteRecord's request/response
shapes are stable, long-established parts of the protocol (unlike the OAuth
profile, which is newer), so this should need less correction than Phase 1
did, but it still hasn't been exercised against a real PDS.
"""

from datetime import datetime, timezone

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.atproto_session import AtprotoSession
from app.utils.atproto_dpop import generate_dpop_proof, public_jwk_from_private_pem
from app.utils.atproto_identity import AtprotoIdentityError, fetch_authorization_server_metadata
from app.utils.atproto_oauth import AtprotoOAuthError, refresh_tokens, token_expiry_from_response

_REFRESH_MARGIN_SECONDS = 60


class AtprotoRepoError(Exception):
    pass


def rkey_from_uri(uri: str) -> str:
    """Extract the record key from an at:// URI (the last path segment)."""
    return uri.rstrip("/").rsplit("/", 1)[-1]


async def get_session_for_user(db: AsyncSession, user_id: int) -> AtprotoSession | None:
    result = await db.execute(select(AtprotoSession).where(AtprotoSession.user_id == user_id))
    return result.scalar_one_or_none()


async def get_valid_session(db: AsyncSession, user_id: int) -> AtprotoSession:
    """Return this user's AtprotoSession, refreshing its access token first
    if it's expired or about to be. Raises AtprotoRepoError if there's no
    session, or if refresh fails (a re-login is then required)."""
    session = await get_session_for_user(db, user_id)
    if session is None:
        raise AtprotoRepoError(f"No AT Protocol session for user {user_id}")

    now = datetime.now(timezone.utc)
    if (session.access_token_expires_at - now).total_seconds() > _REFRESH_MARGIN_SECONDS:
        return session

    if not session.refresh_token:
        raise AtprotoRepoError("AT Protocol session expired and has no refresh token - user must sign in again")

    try:
        as_metadata = await fetch_authorization_server_metadata(session.authorization_server)
    except AtprotoIdentityError as e:
        raise AtprotoRepoError(f"Could not refresh AT Protocol session: {e}") from e

    dpop_public_jwk = public_jwk_from_private_pem(session.dpop_private_key_pem)
    try:
        token_response, new_nonce = await refresh_tokens(
            as_metadata,
            refresh_token=session.refresh_token,
            dpop_private_key_pem=session.dpop_private_key_pem,
            dpop_public_jwk=dpop_public_jwk,
            nonce=session.dpop_authserver_nonce,
        )
    except AtprotoOAuthError as e:
        raise AtprotoRepoError(f"Could not refresh AT Protocol session: {e}") from e

    session.access_token = token_response["access_token"]
    # AT Proto refresh tokens rotate on every use - if we don't persist the
    # new one, the *next* refresh attempt fails with invalid_grant.
    session.refresh_token = token_response.get("refresh_token", session.refresh_token)
    session.access_token_expires_at = datetime.fromtimestamp(
        token_expiry_from_response(token_response), tz=timezone.utc
    )
    session.dpop_authserver_nonce = new_nonce
    session.updated_at = now
    await db.commit()
    await db.refresh(session)
    return session


async def _pds_request_with_dpop_retry(
    client: httpx.AsyncClient, db: AsyncSession, session: AtprotoSession, method: str, url: str, json_body: dict
) -> httpx.Response:
    """Make one DPoP-authenticated call to the PDS, retrying once if it
    demands a fresh nonce (same handshake as the AS token endpoint, but
    against the PDS's own nonce)."""
    dpop_public_jwk = public_jwk_from_private_pem(session.dpop_private_key_pem)

    def make_headers(nonce: str | None) -> dict:
        proof = generate_dpop_proof(
            session.dpop_private_key_pem, dpop_public_jwk, method, url,
            nonce=nonce, access_token=session.access_token,
        )
        return {"Authorization": f"DPoP {session.access_token}", "DPoP": proof}

    resp = await client.request(method, url, json=json_body, headers=make_headers(session.dpop_pds_nonce))
    new_nonce = resp.headers.get("DPoP-Nonce", session.dpop_pds_nonce)

    if resp.status_code in (400, 401) and new_nonce and new_nonce != session.dpop_pds_nonce:
        try:
            if resp.json().get("error") == "use_dpop_nonce":
                resp = await client.request(method, url, json=json_body, headers=make_headers(new_nonce))
                new_nonce = resp.headers.get("DPoP-Nonce", new_nonce)
        except ValueError:
            pass

    if new_nonce != session.dpop_pds_nonce:
        session.dpop_pds_nonce = new_nonce
        await db.commit()

    return resp


async def create_record(db: AsyncSession, session: AtprotoSession, collection: str, record: dict) -> tuple[str, str]:
    """com.atproto.repo.createRecord - lets the PDS mint a new rkey (a TID).
    Returns (at_uri, cid)."""
    url = f"{session.pds_url}/xrpc/com.atproto.repo.createRecord"
    body = {"repo": session.did, "collection": collection, "record": record}

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await _pds_request_with_dpop_retry(client, db, session, "POST", url, body)

    if resp.status_code not in (200, 201):
        raise AtprotoRepoError(f"createRecord failed ({resp.status_code}): {resp.text}")
    data = resp.json()
    return data["uri"], data["cid"]


async def put_record(
    db: AsyncSession, session: AtprotoSession, collection: str, rkey: str, record: dict
) -> tuple[str, str]:
    """com.atproto.repo.putRecord - creates or overwrites the record at a
    specific rkey (used for updates, once a record already exists).
    Returns (at_uri, cid)."""
    url = f"{session.pds_url}/xrpc/com.atproto.repo.putRecord"
    body = {"repo": session.did, "collection": collection, "rkey": rkey, "record": record}

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await _pds_request_with_dpop_retry(client, db, session, "POST", url, body)

    if resp.status_code not in (200, 201):
        raise AtprotoRepoError(f"putRecord failed ({resp.status_code}): {resp.text}")
    data = resp.json()
    return data["uri"], data["cid"]


async def delete_record(db: AsyncSession, session: AtprotoSession, collection: str, rkey: str) -> None:
    """com.atproto.repo.deleteRecord. Deleting a record that's already gone
    is treated as success - the end state (no record) is what we want."""
    url = f"{session.pds_url}/xrpc/com.atproto.repo.deleteRecord"
    body = {"repo": session.did, "collection": collection, "rkey": rkey}

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await _pds_request_with_dpop_retry(client, db, session, "POST", url, body)

    if resp.status_code not in (200, 201, 404):
        raise AtprotoRepoError(f"deleteRecord failed ({resp.status_code}): {resp.text}")
