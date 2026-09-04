from datetime import datetime, timedelta, timezone
import secrets

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.atproto_oauth_request import AtprotoOAuthRequest
from app.models.atproto_session import AtprotoSession
from app.models.users import User
from app.crud import get_or_create_user_for_did, store_refresh_token
from app.services.atproto_sync import sync_all_pending_for_user
from app.utils.atproto_identity import resolve_identity_for_login, fetch_authorization_server_metadata, AtprotoIdentityError
from app.utils.atproto_dpop import generate_dpop_keypair, public_jwk_from_private_pem
from app.utils.atproto_oauth import (
    AtprotoOAuthError,
    build_client_metadata,
    generate_pkce_pair,
    push_authorization_request,
    build_authorization_url,
    exchange_code_for_tokens,
    token_expiry_from_response,
)
from app.utils.security import create_access_token, create_refresh_token

router = APIRouter(prefix="/auth/atproto", tags=["Auth - AT Protocol"])


def _require_configured():
    if not (settings.ATPROTO_CLIENT_ID and settings.ATPROTO_REDIRECT_URI):
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="AT Protocol login is not configured on this server "
                   "(ATPROTO_CLIENT_ID / ATPROTO_REDIRECT_URI unset).",
        )


@router.get("/client-metadata.json")
async def client_metadata():
    _require_configured()
    return JSONResponse(build_client_metadata())


class StartLoginRequest(BaseModel):
    handle: str


@router.post("/start", status_code=status.HTTP_200_OK)
async def start_login(body: StartLoginRequest, db: AsyncSession = Depends(get_db)):
    """Resolve the user's handle to their PDS, push an authorization
    request, and hand back the URL the frontend should redirect the
    browser to."""
    _require_configured()

    try:
        identity = await resolve_identity_for_login(body.handle)
    except AtprotoIdentityError as e:
        raise HTTPException(status_code=400, detail=str(e))

    state = secrets.token_urlsafe(32)
    code_verifier, code_challenge = generate_pkce_pair()
    dpop_private_key_pem, dpop_public_jwk = generate_dpop_keypair()

    try:
        request_uri, nonce = await push_authorization_request(
            identity["as_metadata"],
            dpop_private_key_pem,
            dpop_public_jwk,
            login_hint=body.handle,
            state=state,
            code_challenge=code_challenge,
        )
    except AtprotoOAuthError as e:
        raise HTTPException(status_code=502, detail=f"Could not start AT Protocol login: {e}")

    db.add(AtprotoOAuthRequest(
        state=state,
        handle=body.handle,
        did=identity["did"],
        pds_url=identity["pds_url"],
        authorization_server=identity["authorization_server"],
        pkce_code_verifier=code_verifier,
        dpop_private_key_pem=dpop_private_key_pem,
        dpop_authserver_nonce=nonce,
        created_at=datetime.now(timezone.utc),
    ))
    await db.commit()

    authorization_url = build_authorization_url(identity["as_metadata"], request_uri)
    return {"authorization_url": authorization_url}


@router.get("/callback")
async def callback(code: str, state: str, iss: str, db: AsyncSession = Depends(get_db)):
    """The PDS redirects the user's browser back here after they approve
    (or deny) the login on their own authorization server."""
    _require_configured()

    result = await db.execute(select(AtprotoOAuthRequest).where(AtprotoOAuthRequest.state == state))
    oauth_request = result.scalar_one_or_none()
    if not oauth_request:
        raise HTTPException(status_code=400, detail="Unknown or expired login attempt")

    # Mix-up attack defense (RFC 9207): the AS that answers the callback must
    # be the same one we sent the PAR to. Skipping this lets a malicious or
    # compromised authorization server mint a session under a different
    # identity than the one the user actually authenticated with.
    if iss != oauth_request.authorization_server:
        await db.delete(oauth_request)
        await db.commit()
        raise HTTPException(status_code=400, detail="Authorization server mismatch")

    # Abandoned/stale attempts (>10 min) shouldn't be redeemable.
    if datetime.now(timezone.utc) - oauth_request.created_at > timedelta(minutes=10):
        await db.delete(oauth_request)
        await db.commit()
        raise HTTPException(status_code=400, detail="Login attempt expired, please try again")

    try:
        as_metadata = await fetch_authorization_server_metadata(oauth_request.authorization_server)
    except AtprotoIdentityError as e:
        raise HTTPException(status_code=502, detail=str(e))

    dpop_public_jwk = public_jwk_from_private_pem(oauth_request.dpop_private_key_pem)

    try:
        token_response, _nonce = await exchange_code_for_tokens(
            as_metadata,
            code=code,
            code_verifier=oauth_request.pkce_code_verifier,
            dpop_private_key_pem=oauth_request.dpop_private_key_pem,
            dpop_public_jwk=dpop_public_jwk,
            nonce=oauth_request.dpop_authserver_nonce,
        )
    except AtprotoOAuthError as e:
        await db.delete(oauth_request)
        await db.commit()
        raise HTTPException(status_code=502, detail=f"AT Protocol token exchange failed: {e}")

    # Same defense as the `iss` check above, at the token-exchange step: the
    # tokens must have actually been issued for the DID we resolved before
    # redirecting, not some other account the AS decided to authenticate.
    if token_response.get("sub") != oauth_request.did:
        await db.delete(oauth_request)
        await db.commit()
        raise HTTPException(status_code=400, detail="Token subject does not match resolved DID")

    user = await get_or_create_user_for_did(
        db, did=oauth_request.did, pds_url=oauth_request.pds_url, handle=oauth_request.handle
    )

    existing = await db.execute(select(AtprotoSession).where(AtprotoSession.user_id == user.id))
    session_row = existing.scalar_one_or_none()
    now = datetime.now(timezone.utc)
    expires_at = datetime.fromtimestamp(token_expiry_from_response(token_response), tz=timezone.utc)

    if session_row:
        session_row.did = oauth_request.did
        session_row.pds_url = oauth_request.pds_url
        session_row.authorization_server = oauth_request.authorization_server
        session_row.access_token = token_response["access_token"]
        session_row.refresh_token = token_response.get("refresh_token")
        session_row.access_token_expires_at = expires_at
        session_row.dpop_private_key_pem = oauth_request.dpop_private_key_pem
        session_row.dpop_authserver_nonce = oauth_request.dpop_authserver_nonce
        session_row.updated_at = now
    else:
        db.add(AtprotoSession(
            user_id=user.id,
            did=oauth_request.did,
            pds_url=oauth_request.pds_url,
            authorization_server=oauth_request.authorization_server,
            access_token=token_response["access_token"],
            refresh_token=token_response.get("refresh_token"),
            access_token_expires_at=expires_at,
            dpop_private_key_pem=oauth_request.dpop_private_key_pem,
            dpop_authserver_nonce=oauth_request.dpop_authserver_nonce,
            created_at=now,
            updated_at=now,
        ))

    await db.delete(oauth_request)
    await db.commit()

    # From here on, the user is signed in exactly like a password login: our
    # own short-lived access/refresh cookies, so the rest of the app
    # (get_current_user, fetchWithAuth's 401 retry, etc.) needs no changes.
    access_token = create_access_token(user_id=user.id, expires_delta=timedelta(minutes=30))
    refresh_token = create_refresh_token(user_id=user.id, expires_delta=timedelta(days=7))
    await store_refresh_token(db, user_id=user.id, token=refresh_token)

    redirect_target = f"{(settings.ATPROTO_CLIENT_URI or '').rstrip('/')}/profile"
    response = RedirectResponse(url=redirect_target, status_code=status.HTTP_302_FOUND)
    response.set_cookie(
        key="access_token", value=access_token, httponly=True, samesite="none", secure=True, max_age=1800,
    )
    response.set_cookie(
        key="refresh_token", value=refresh_token, httponly=True, samesite="none", secure=True,
        max_age=7 * 24 * 60 * 60,
    )
    return response


class SyncToggleRequest(BaseModel):
    enabled: bool


@router.patch("/sync")
async def set_sync_enabled(
    body: SyncToggleRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Opt this user in/out of Phase 2 dual-write (see
    AT_PROTOCOL_MIGRATION.md section 10). Requires an AT Proto identity -
    there's nowhere to write records without one."""
    if not current_user.did:
        raise HTTPException(
            status_code=400,
            detail="AT Protocol dual-write requires signing in with AT Protocol first",
        )

    current_user.atproto_sync_enabled = body.enabled
    await db.commit()
    return {"atproto_sync_enabled": current_user.atproto_sync_enabled}


@router.post("/sync-pending")
async def sync_pending(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Retry every record that failed to sync to the PDS on its first
    attempt. This is the manual "sync now" surface for the outbox pattern in
    AT_PROTOCOL_MIGRATION.md section 7 - equally callable from a cron/worker
    once one exists, since it just re-runs the same best-effort sync
    functions the write-path background tasks use."""
    counts = await sync_all_pending_for_user(db, current_user)
    return {"synced": counts}
