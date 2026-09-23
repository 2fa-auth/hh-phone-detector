import re
from collections.abc import Iterable

from .normalizer import NormalizedPhone, normalize_phone


# Regex only finds candidates.
# phonenumbers + contextual checks decide whether they are phones.
PHONE_CANDIDATE_RE = re.compile(
    r"(?<!\d)(?:\+\d[\d\s().\-]{6,}\d|\d[\d\s().\-]{6,}\d)(?!\d)"
)

PHONE_KEYS = {
    "phone",
    "phones",
    "phonenumber",
    "phone_number",
    "phonenumber",
    "phoneNumber",
}


# Obvious contexts where a long digit sequence is an identifier,
# not a phone number.
NON_PHONE_CONTEXT_RE = re.compile(
    r"""
    (?:
        \b(?:vacancy|ваканс(?:ия|ии|ию|ией|ию))\s*(?:id|№|номер)?
        |
        \b(?:id|идентификатор|артикул|сборка|release|project|портфолио)
        |
        [#№]
    )
    \s*[:#№=\-]?\s*$
    """,
    re.IGNORECASE | re.VERBOSE,
)


def _find_phone_strings(value: object, key: str | None = None) -> Iterable[str]:
    """
    Extract phone strings from HH-like structured contacts.

    Once we enter a phone-related field, nested string values are treated
    as phone candidates.
    """
    if isinstance(value, str):
        if key in PHONE_KEYS or key == "value":
            yield value
        return

    if isinstance(value, dict):
        for child_key, child_value in value.items():
            normalized_key = str(child_key).replace("-", "_").lower()

            if normalized_key in PHONE_KEYS:
                yield from _find_phone_strings(child_value, normalized_key)
            elif key in PHONE_KEYS:
                yield from _find_phone_strings(child_value, key)
            elif isinstance(child_value, (dict, list, tuple)):
                yield from _find_phone_strings(child_value, normalized_key)

        return

    if isinstance(value, (list, tuple)):
        for item in value:
            yield from _find_phone_strings(item, key)


def extract_candidates(text: str) -> list[str]:
    if not text:
        return []

    return [
        match.group(0).strip()
        for match in PHONE_CANDIDATE_RE.finditer(text)
    ]


def _is_obvious_identifier(text: str, candidate: str) -> bool:
    """
    Reject candidates that are clearly presented as identifiers.

    Example:
        Vacancy ID: 79991234567
        Артикул 89991234567
        Сборка #79991234567
        project-79991234567

    We intentionally keep this conservative: ordinary phone-looking
    numbers are not rejected just because they are long.
    """
    start = text.find(candidate)

    if start == -1:
        return False

    prefix = text[max(0, start - 40):start]

    # Look at the immediate text before the number.
    # We only reject when the number is explicitly attached to an
    # identifier-like label.
    if re.search(
        r"(?:vacancy\s+id|id|идентификатор|артикул|сборка|release|project|портфолио|вакансия\s*(?:№|id|номер)?)"
        r"\s*[:#№=\-]?\s*$",
        prefix,
        re.IGNORECASE,
    ):
        return True

    # Explicit "#" / "№" immediately before the number.
    if re.search(r"[#№]\s*$", prefix):
        return True

    return False


def _extract_from_text(
    text: str,
    default_region: str,
) -> list[NormalizedPhone]:
    result: list[NormalizedPhone] = []

    for candidate in extract_candidates(text):
        if _is_obvious_identifier(text, candidate):
            continue

        phone = normalize_phone(candidate, default_region)

        if phone:
            result.append(phone)

    return result


def extract_valid_phones(
    description: str,
    contacts: object | None,
    default_region: str = "RU",
) -> list[tuple[NormalizedPhone, str]]:
    """
    Return (normalized_phone, source) pairs.

    Structured contacts are processed first. Description is processed second.
    Duplicate normalized numbers are removed while preserving first occurrence.
    """
    found: dict[str, tuple[NormalizedPhone, str]] = {}

    # Structured HH contacts.
    for raw in _find_phone_strings(contacts):
        for candidate in extract_candidates(raw):
            phone = normalize_phone(candidate, default_region)

            if phone and phone.normalized not in found:
                found[phone.normalized] = (phone, "contacts")

    # Vacancy description.
    for candidate in extract_candidates(description):
        if _is_obvious_identifier(description, candidate):
            continue

        phone = normalize_phone(candidate, default_region)

        if phone and phone.normalized not in found:
            found[phone.normalized] = (phone, "description")

    return list(found.values())
