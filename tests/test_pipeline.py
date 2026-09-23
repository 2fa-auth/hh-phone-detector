from app.models import VacancyInput
from app.pipeline import PhoneAnalyzer, analyze_batch


def test_analyzer_output():
    vacancy = VacancyInput(
        id="123",
        url="https://hh.ru/vacancy/123",
        title="Developer",
        company="Test",
        description="Телефон +7 999 123-45-67",
    )

    result = PhoneAnalyzer().analyze(vacancy)

    assert result.vacancy_id == "123"
    assert result.has_phone is True
    assert result.phones[0].normalized == "+79991234567"


def test_batch_does_not_stop_on_bad_vacancy():
    analyzer = PhoneAnalyzer()

    vacancies = [
        VacancyInput(
            id="1",
            description="Телефон +7 999 123-45-67",
        ),
        VacancyInput(
            id="2",
            description="Без телефона",
        ),
    ]

    results, errors = analyze_batch(vacancies, analyzer)

    assert len(results) == 2
    assert errors == []
