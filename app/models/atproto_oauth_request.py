from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, Text
from app.database import Base
from typing import Optional


class AtprotoOAuthRequest(Base):
    """Short-lived state for one in-flight AT Protocol OAuth authorization
    attempt.

    Our API is the OAuth client, so it (not the browser) holds the PKCE
    verifier and the DPoP keypair between the moment we redirect the user to
    their PDS's authorization page and the moment they're redirected back to
    our /auth/atproto/callback. Rows here should be deleted once consumed by
    the callback, and a background cleanup should also purge anything older
    than a few minutes (abandoned logins).
    """

    __tablename__ = "atproto_oauth_requests"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    state: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)

    handle: Mapped[str] = mapped_column(nullable=False)
    did: Mapped[Optional[str]] = mapped_column(nullable=True)
    pds_url: Mapped[str] = mapped_column(nullable=False)
    authorization_server: Mapped[str] = mapped_column(nullable=False)

    pkce_code_verifier: Mapped[str] = mapped_column(nullable=False)
    dpop_private_key_pem: Mapped[str] = mapped_column(Text, nullable=False)
    dpop_authserver_nonce: Mapped[Optional[str]] = mapped_column(nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
