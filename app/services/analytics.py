from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from sqlalchemy.orm import selectinload
from datetime import datetime, timezone
from app.models.location import VisitedLocation, WishlistLocation

async def get_proposed_trip(user_id: int, db: AsyncSession):
    result = await db.execute(
        select(WishlistLocation)
        .where(
            WishlistLocation.owner_id == user_id,
            WishlistLocation.proposed_date.isnot(None),
            WishlistLocation.proposed_date > datetime.now(timezone.utc)
        )
        .order_by(WishlistLocation.proposed_date.asc())
        .limit(1)
    )
    return result.scalar_one_or_none()
async def get_user_analytics(user_id: int, db: AsyncSession) -> dict:
    
    countries_query = await db.execute(
        select(func.count(func.distinct(WishlistLocation.country)))
        .select_from(VisitedLocation)
        .join(WishlistLocation, VisitedLocation.wishlist_id == WishlistLocation.id)
        .where(VisitedLocation.owner_id == user_id)
    )
    countries_visited = countries_query.scalar() or 0

    cities_query = await db.execute(
        select(func.count(func.distinct(WishlistLocation.city)))
        .select_from(VisitedLocation)
        .join(WishlistLocation, VisitedLocation.wishlist_id == WishlistLocation.id)
        .where(VisitedLocation.owner_id == user_id)
    )
    cities_visited = cities_query.scalar() or 0

    wishlist_query = await db.execute(
        select(func.count()).where(WishlistLocation.owner_id == user_id, WishlistLocation.visited == False)
    )
    wishlist_remaining = wishlist_query.scalar() or 0

    most_visited_query = await db.execute(
        select(WishlistLocation.country, func.count().label("visit_count"))
        .select_from(VisitedLocation)
        .join(WishlistLocation, VisitedLocation.wishlist_id == WishlistLocation.id)
        .where(VisitedLocation.owner_id == user_id)
        .group_by(WishlistLocation.country)
        .order_by(desc("visit_count"))
        .limit(1)
    )
    most_visited_row = most_visited_query.first()
    most_visited_country = most_visited_row[0] if most_visited_row else None

    highest_rated_query = await db.execute(
        select(
            WishlistLocation.name,
            WishlistLocation.city,
            WishlistLocation.country,
            VisitedLocation.rating
        )
        .select_from(VisitedLocation)
        .join(WishlistLocation, VisitedLocation.wishlist_id == WishlistLocation.id)
        .where(
            VisitedLocation.owner_id == user_id,
            VisitedLocation.rating.isnot(None)
        )
        .order_by(desc(VisitedLocation.rating))
        .limit(1)
    )

    highest_rated_row = highest_rated_query.first()
    highest_rated_trip = {
        "name": highest_rated_row[0],
        "city": highest_rated_row[1],
        "country": highest_rated_row[2],
        "rating": highest_rated_row[3],
    } if highest_rated_row else None

    recent_trip_query = await db.execute(
        select(VisitedLocation)
        .options(selectinload(VisitedLocation.wishlist_location))
        .where(VisitedLocation.owner_id == user_id)
        .order_by(desc(VisitedLocation.visited_on))
        .limit(1)
    )
    recent_trip = recent_trip_query.scalar_one_or_none()

    days_since_last_trip = None
    if recent_trip and recent_trip.visited_on:
        now = datetime.now(timezone.utc)
        days_since_last_trip = (now - recent_trip.visited_on).days
    
    upcoming = await get_proposed_trip(user_id, db)

    nearest_upcoming_trip = {
        "name": upcoming.name,
        "city": upcoming.city,
        "country": upcoming.country,
        "proposed_date": upcoming.proposed_date,
        "notes": upcoming.notes,
    }   if upcoming else None

    return {
        "nearest_upcoming_trip": nearest_upcoming_trip,
        "most_recent_trip": {
            "name": recent_trip.wishlist_location.name if recent_trip else None,
            "city": recent_trip.wishlist_location.city if recent_trip else None,
            "country": recent_trip.wishlist_location.country if recent_trip else None,
            "visited_on": recent_trip.visited_on if recent_trip else None,
            "rating": recent_trip.rating if recent_trip else None,
        } if recent_trip else None,
        "days_since_last_trip": days_since_last_trip,
        "highest_rated_trip": highest_rated_trip,
        "countries_visited": countries_visited,
        "cities_visited": cities_visited,
        "wishlist_remaining": wishlist_remaining,
        "most_visited_country": most_visited_country,
    }
