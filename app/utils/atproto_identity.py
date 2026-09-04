"""AT Protocol identity resolution: handle -> DID -> PDS -> authorization server.

There's no central AT Proto login server - every user's PDS is its own OAuth
authorization server, so before we can start an OAuth flow we have to work
out, from the handle the user typed in, which server to actually talk to.

NOTE ON VERIFICATION: this follows the AT Protocol identity/OAuth spec as
understood at implementation time. atproto.com and docs.bsky.app were not
reachable from this environment to pin exact field names/well-known paths
against the live spec, so double-check this module (particularly the
well-known discovery paths and PLC directory shape) against
https://atproto.com/specs/oauth and https://atproto.com/specs/did before
this touches a production login flow.
"""

import httpx

PLC_DIRECTORY_URL = "https://plc.directory"


class AtprotoIdentityError(Exception):
    pass


async def resolve_handle_to_did(handle: str) -> str:
    """Resolve a handle (e.g. alice.bsky.social) to a DID.

    Tries the public Bluesky XRPC endpoint first (works for any handle
    regardless of which PDS it lives on, since resolveHandle just does the
    DNS/.well-known lookup for us); falls back to querying the handle's own
    domain directly if that fails.
    """
    handle = handle.strip().lstrip("@")

    async with httpx.AsyncClient(timeout=10) as client:
        try:
            resp = await client.get(
                "https://public.api.bsky.app/xrpc/com.atproto.identity.resolveHandle",
                params={"handle": handle},
            )
            if resp.status_code == 200:
                did = resp.json().get("did")
                if did:
                    return did
        except httpx.HTTPError:
            pass

        # Fallback: DNS-free HTTPS well-known check on the handle's own domain.
        try:
            resp = await client.get(f"https://{handle}/.well-known/atproto-did")
            if resp.status_code == 200:
                did = resp.text.strip()
                if did.startswith("did:"):
                    return did
        except httpx.HTTPError:
            pass

    raise AtprotoIdentityError(f"Could not resolve handle '{handle}' to a DID")


async def resolve_did_document(did: str) -> dict:
    """Fetch a DID document for a did:plc or did:web identifier."""
    async with httpx.AsyncClient(timeout=10) as client:
        if did.startswith("did:plc:"):
            resp = await client.get(f"{PLC_DIRECTORY_URL}/{did}")
        elif did.startswith("did:web:"):
            domain = did.removeprefix("did:web:").replace(":", "/")
            resp = await client.get(f"https://{domain}/.well-known/did.json")
        else:
            raise AtprotoIdentityError(f"Unsupported DID method: {did}")

        if resp.status_code != 200:
            raise AtprotoIdentityError(f"Failed to resolve DID document for {did}")
        return resp.json()


def get_pds_url_from_did_document(did_doc: dict) -> str:
    for service in did_doc.get("service", []):
        if service.get("id") in ("#atproto_pds", f"{did_doc.get('id')}#atproto_pds"):
            endpoint = service.get("serviceEndpoint")
            if endpoint:
                return endpoint.rstrip("/")
    raise AtprotoIdentityError("DID document has no #atproto_pds service entry")


async def resolve_pds_authorization_server(pds_url: str) -> str:
    """Given a PDS base URL, find the issuer URL of its OAuth authorization
    server via the standard protected-resource metadata document."""
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(f"{pds_url}/.well-known/oauth-protected-resource")
        if resp.status_code != 200:
            raise AtprotoIdentityError(f"Failed to fetch protected-resource metadata from {pds_url}")
        servers = resp.json().get("authorization_servers") or []
        if not servers:
            raise AtprotoIdentityError(f"PDS {pds_url} advertised no authorization servers")
        return servers[0]


async def fetch_authorization_server_metadata(issuer: str) -> dict:
    """Fetch the OAuth authorization server's metadata document (endpoints
    for pushed authorization requests, authorize, and token)."""
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(f"{issuer.rstrip('/')}/.well-known/oauth-authorization-server")
        if resp.status_code != 200:
            raise AtprotoIdentityError(f"Failed to fetch authorization server metadata from {issuer}")
        return resp.json()


async def resolve_identity_for_login(handle: str) -> dict:
    """Full handle -> {did, pds_url, authorization_server, as_metadata} resolution."""
    did = await resolve_handle_to_did(handle)
    did_doc = await resolve_did_document(did)
    pds_url = get_pds_url_from_did_document(did_doc)
    issuer = await resolve_pds_authorization_server(pds_url)
    as_metadata = await fetch_authorization_server_metadata(issuer)
    return {
        "did": did,
        "pds_url": pds_url,
        "authorization_server": issuer,
        "as_metadata": as_metadata,
    }
