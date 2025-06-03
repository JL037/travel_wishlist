from sqlalchemy import Integer, String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.users import User

class TravelPlan(Base):
    __tablename__ = "travel_plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    date: Mapped[Date]
    location: Mapped[str]
    notes: Mapped[str | None] = mapped_column(nullable=False)

    user: Mapped["User"] = relationship(back_populates="travel_plans")