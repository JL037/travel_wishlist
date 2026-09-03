from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime, Text
from app.database import Base
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.models.users import User


class AtprotoSession(Base):
    """A user's live OAuth session against their own PDS.

    One row per user (mirrors the single-active-token pattern used by
    RefreshToken). Holds what's needed to make DPoP-bound XRPC calls to the
    user's PDS on their behalf between requests: the token pair, the DPoP
    keypair those tokens are bound to, and the last nonce the authorization
    server handed back (DPoP requires echoing the server's latest nonce on
    each request or the call is rejected).

    access_token / refresh_token / dpop_private_key_pem are sensitive and
    should be encrypted at rest before this goes to production - stored as
    plain text here only as a Phase 1 scaffold.
    """

    __tablename__ = "atproto_sessions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True
    )

    did: Mapped[str] = mapped_column(nullable=False, index=True)
    pds_url: Mapped[str] = mapped_column(nullable=False)
    authorization_server: Mapped[str] = mapped_column(nullable=False)

    access_token: Mapped[str] = mapped_column(Text, nullable=False)
    refresh_token: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    access_token_expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    # PEM-encoded EC P-256 private key this session's tokens are DPoP-bound to.
    dpop_private_key_pem: Mapped[str] = mapped_column(Text, nullable=False)
    dpop_authserver_nonce: Mapped[Optional[str]] = mapped_column(nullable=True)
    dpop_pds_nonce: Mapped[Optional[str]] = mapped_column(nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    user: Mapped["User"] = relationship(back_populates="atproto_session")
