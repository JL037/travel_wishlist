# app/seeds/seed_db.py
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.users import User
from app.models.location import WishlistLocation
from app.models.location import VisitedLocation
from app.utils.security import hash_password
from datetime import timezone, datetime


def seed():
    print("Seeding the database...")
    db: Session = SessionLocal()

    # Clear old data
    db.query(VisitedLocation).delete()
    db.query(WishlistLocation).delete()
    db.query(User).delete()
    db.commit()

    # Create user
    user = User(email="test@example.com", hashed_password=hash_password("password123"))
    db.add(user)
    db.commit()
    db.refresh(user)

    # Wishlist (not visited)
    wishlist = WishlistLocation(
        name="Paris",
        city="Paris",
        country="France",
        visited=True,
        owner_id=user.id,
        latitude=48.8566,
        longitude=2.3522,
    )

    db.add(wishlist)
    db.commit()
    db.refresh(wishlist)

    visited = VisitedLocation(
        wishlist_id=wishlist.id,
        owner_id=user.id,
        visited_on=datetime.now(timezone.utc),
        notes="Beautiful trip!",
        rating=5,
    )

    db.add(visited)
    db.commit()

    db.add_all([wishlist, visited])
    db.commit()
    db.close()
    print("✅ Seeded DB with 1 user, 1 wishlist, 1 visited")


if __name__ == "__main__":
    seed()
