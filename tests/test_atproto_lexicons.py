from datetime import date, datetime, timezone
from types import SimpleNamespace

from app.utils.atproto_lexicons import (
    TRAVEL_PLAN_COLLECTION,
    VISITED_LOCATION_COLLECTION,
    WISHLIST_LOCATION_COLLECTION,
    travel_plan_to_record,
    visited_location_to_record,
    wishlist_location_to_record,
)


def _wishlist_location(**overrides):
    defaults = dict(
        name="Eiffel Tower trip",
        city="Paris",
        country="France",
        latitude=48.8566,
        longitude=2.3522,
        proposed_date=None,
        added_on=datetime(2026, 1, 1, tzinfo=timezone.utc),
        atproto_record_uri=None,
        atproto_record_cid=None,
    )
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


def test_wishlist_location_to_record_required_fields():
    location = _wishlist_location(name=None)
    record = wishlist_location_to_record(location)

    assert record["$type"] == WISHLIST_LOCATION_COLLECTION
    assert record["city"] == "Paris"
    assert record["country"] == "France"
    assert record["createdAt"] == "2026-01-01T00:00:00Z"
    assert "name" not in record


def test_wishlist_location_to_record_optional_fields_included_when_present():
    location = _wishlist_location(proposed_date=datetime(2026, 6, 1, tzinfo=timezone.utc))
    record = wishlist_location_to_record(location)

    assert record["name"] == "Eiffel Tower trip"
    assert record["latitude"] == 48.8566
    assert record["longitude"] == 2.3522
    assert record["proposedDate"] == "2026-06-01T00:00:00Z"


def test_wishlist_location_to_record_naive_datetime_treated_as_utc():
    location = _wishlist_location(added_on=datetime(2026, 1, 1))  # no tzinfo
    record = wishlist_location_to_record(location)
    assert record["createdAt"] == "2026-01-01T00:00:00Z"


def test_visited_location_to_record_falls_back_to_wishlist_lat_lon():
    wishlist_location = _wishlist_location()
    visited = SimpleNamespace(
        latitude=None,
        longitude=None,
        rating=None,
        visited_on=datetime(2026, 3, 1, tzinfo=timezone.utc),
        atproto_record_uri=None,
    )

    record = visited_location_to_record(visited, wishlist_location)

    assert record["$type"] == VISITED_LOCATION_COLLECTION
    assert record["city"] == "Paris"
    assert record["country"] == "France"
    assert record["latitude"] == 48.8566
    assert record["longitude"] == 2.3522
    assert "rating" not in record
    assert "wishlistUri" not in record


def test_visited_location_to_record_includes_strong_ref_when_given():
    wishlist_location = _wishlist_location()
    visited = SimpleNamespace(
        latitude=1.0, longitude=2.0, rating=5,
        visited_on=datetime(2026, 3, 1, tzinfo=timezone.utc),
        atproto_record_uri=None,
    )

    record = visited_location_to_record(
        visited, wishlist_location,
        wishlist_ref=("at://did:plc:abc/app.travelwishlist.wishlist.location/xyz", "bafyabc"),
    )

    assert record["rating"] == 5
    assert record["wishlistUri"] == {
        "$type": "com.atproto.repo.strongRef",
        "uri": "at://did:plc:abc/app.travelwishlist.wishlist.location/xyz",
        "cid": "bafyabc",
    }


def test_travel_plan_to_record():
    plan = SimpleNamespace(location="Tokyo", start_date=date(2026, 4, 1), end_date=date(2026, 4, 10))
    record = travel_plan_to_record(plan)

    assert record == {
        "$type": TRAVEL_PLAN_COLLECTION,
        "location": "Tokyo",
        "startDate": "2026-04-01T00:00:00Z",
        "endDate": "2026-04-10T00:00:00Z",
    }
