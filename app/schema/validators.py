

def strip_and_validate_not_empty(value: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError("Field must not be blank or only whitespace")
    return cleaned


def validate_country_format(value: str) -> str:
    if not value.isalpha() or len(value.strip()) < 2:
        raise ValueError(
            "Country name must contain only letters and must be at least 2 characters"
        )
    return value.strip()


def validate_latitude(value: float) -> float:
    if value < -90 or value > 90:
        raise ValueError("Latitude must be between -90 and 90")
    return value


def validate_longitude(value: float) -> float:
    if value < -180 or value > 180:
        raise ValueError("Longitude must be between -180 and 180")
    return value
