from collections.abc import Iterable

from .models import PhoneContact, VacancyInput, VacancyPhoneResult
from .phones.extractor import extract_valid_phones


class PhoneAnalyzer:
    def __init__(self, default_region: str = "RU"):
        self.default_region = default_region

    def analyze(self, vacancy: VacancyInput) -> VacancyPhoneResult:
        phones = extract_valid_phones(
            description=vacancy.description,
            contacts=vacancy.contacts,
            default_region=self.default_region,
        )

        return VacancyPhoneResult(
            vacancy_id=vacancy.id,
            url=vacancy.url,
            title=vacancy.title,
            company=vacancy.company,
            has_phone=bool(phones),
            phones=[
                PhoneContact(
                    raw=phone.raw,
                    normalized=phone.normalized,
                    source=source,
                )
                for phone, source in phones
            ],
        )


def analyze_batch(
    vacancies: Iterable[VacancyInput],
    analyzer: PhoneAnalyzer,
) -> tuple[list[VacancyPhoneResult], list[dict[str, str]]]:
    results: list[VacancyPhoneResult] = []
    errors: list[dict[str, str]] = []

    for vacancy in vacancies:
        try:
            results.append(analyzer.analyze(vacancy))
        except Exception as exc:
            errors.append(
                {
                    "vacancy_id": vacancy.id,
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )

    return results, errors
