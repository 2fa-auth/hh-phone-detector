from dataclasses import dataclass

import phonenumbers
from phonenumbers import NumberParseException


@dataclass(frozen=True)
class NormalizedPhone:
    raw: str
    normalized: str


def normalize_phone(raw: str, default_region: str = "RU") -> NormalizedPhone | None:
    """
    Parse and validate a candidate phone number.

    Returns E.164 representation only for valid phone numbers.
    """
    value = raw.strip()
    if not value:
        return None

    try:
        parsed = phonenumbers.parse(value, default_region)
    except NumberParseException:
        return None

    if not phonenumbers.is_possible_number(parsed):
        return None

    if not phonenumbers.is_valid_number(parsed):
        return None

    normalized = phonenumbers.format_number(
        parsed,
        phonenumbers.PhoneNumberFormat.E164,
    )
    return NormalizedPhone(raw=value, normalized=normalized)
