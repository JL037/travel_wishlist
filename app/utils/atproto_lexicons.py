"""Builders for the app.travelwishlist.* Lexicon record shapes: pure
functions mapping our local models to the public-fields-only records
written to a user's PDS repo. Must match the Lexicon definitions in
AT_PROTOCOL_MIGRATION.md section 5.

Only public fields cross this boundary - `notes`/`description` on the local
models never appear in these records; that split is the whole point of the
dual-write design (see AT_PROTOCOL_MIGRATION.md section 7).
"""

from datetime import date, datetime, timezone

WISHLIST_LOCATION_COLLECTION = "app.travelwishlist.wishlist.location"
VISITED_LOCATION_COLLECTION = "app.travelwishlist.visited.location"
TRAVEL_PLAN_COLLECTION = "app.travelwishlist.travelPlan"


def _iso(value: datetime | date | None) -> str | None:
    """Format a datetime/date as the AT Proto Lexicon `datetime` format:
    RFC 3339 / ISO 8601 with an explicit UTC offset."""
    if value is None:
        return None
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.isoformat().replace("+00:00", "Z")
    if isinstance(value, date):
        return datetime(value.year, value.month, value.day, tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")
    raise TypeError(f"Cannot format {value!r} as an AT Proto datetime")


def wishlist_location_to_record(location) -> dict:
    """Build an app.travelwishlist.wishlist.location record from a
    WishlistLocation row (app/models/location.py)."""
    record = {
        "$type": WISHLIST_LOCATION_COLLECTION,
        "city": location.city,
        "country": location.country,
        "createdAt": _iso(location.added_on) or _iso(datetime.now(timezone.utc)),
    }
    if location.name:
        record["name"] = location.name
    if location.latitude is not None:
        record["latitude"] = location.latitude
    if location.longitude is not None:
        record["longitude"] = location.longitude
    if location.proposed_date:
        record["proposedDate"] = _iso(location.proposed_date)
    return record


def visited_location_to_record(visited, wishlist_location, wishlist_ref: tuple[str, str] | None = None) -> dict:
    """Build an app.travelwishlist.visited.location record.

    `wishlist_location` supplies city/country - VisitedLocation itself
    doesn't store them, it joins to WishlistLocation for that (see
    app/routers/visited.py). `wishlist_ref` is the (uri, cid) of the
    corresponding wishlist record if it's already been synced to the PDS;
    the Lexicon's `wishlistUri` strongRef is only included when we have one
    (sync order: wishlist record first, then visited, so this is normally
    available - see app/services/atproto_sync.py).
    """
    record = {
        "$type": VISITED_LOCATION_COLLECTION,
        "city": wishlist_location.city,
        "country": wishlist_location.country,
        "visitedOn": _iso(visited.visited_on),
    }
    latitude = visited.latitude if visited.latitude is not None else wishlist_location.latitude
    longitude = visited.longitude if visited.longitude is not None else wishlist_location.longitude
    if latitude is not None:
        record["latitude"] = latitude
    if longitude is not None:
        record["longitude"] = longitude
    if visited.rating is not None:
        record["rating"] = visited.rating
    if wishlist_ref:
        uri, cid = wishlist_ref
        record["wishlistUri"] = {"$type": "com.atproto.repo.strongRef", "uri": uri, "cid": cid}
    return record


def travel_plan_to_record(plan) -> dict:
    """Build an app.travelwishlist.travelPlan record from a TravelPlan row."""
    return {
        "$type": TRAVEL_PLAN_COLLECTION,
        "location": plan.location,
        "startDate": _iso(plan.start_date),
        "endDate": _iso(plan.end_date),
    }
