from sqlalchemy import Integer, String, Date, ForeignKey, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from datetime import datetime
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.models.users import User

class TravelPlan(Base):
    __tablename__ = "travel_plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    start_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    end_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    location: Mapped[str] = mapped_column(String, nullable=False)
    notes: Mapped[str | None] = mapped_column(String, nullable=True)

    # Same Phase 2 bookkeeping as WishlistLocation, for the corresponding
    # app.travelwishlist.travelPlan record. `notes` stays local-only.
    atproto_record_uri: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    atproto_record_cid: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    atproto_sync_pending: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")
    atproto_sync_error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    user: Mapped["User"] = relationship(back_populates="travel_plans")
