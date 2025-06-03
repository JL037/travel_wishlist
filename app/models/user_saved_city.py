from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey, String
from app.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models import User


class UserSavedCity(Base):
    __tablename__ = "user_saved_cities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    city: Mapped[str] = mapped_column(String, nullable=False)

    user: Mapped["User"] = relationship(back_populates="saved_cities")