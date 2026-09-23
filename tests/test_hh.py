from app.sources.hh import HHClient


def test_map_hh_vacancy():
    payload = {
        "id": 12345,
        "name": "Python Developer",
        "alternate_url": "https://hh.ru/vacancy/12345",
        "employer": {
            "name": "Example Company",
        },
        "description": "Звоните +7 999 123-45-67",
        "contacts": {
            "phones": [
                {
                    "value": "+7 999 123-45-67",
                }
            ]
        },
    }

    vacancy = HHClient._map_vacancy(payload)

    assert vacancy.id == "12345"
    assert vacancy.title == "Python Developer"
    assert vacancy.company == "Example Company"
    assert vacancy.url == "https://hh.ru/vacancy/12345"
    assert vacancy.description == "Звоните +7 999 123-45-67"
    assert vacancy.contacts["phones"][0]["value"] == "+7 999 123-45-67"


def test_map_hh_vacancy_handles_missing_optional_fields():
    payload = {
        "id": 12345,
        "name": "Developer",
        "employer": None,
        "description": None,
    }

    vacancy = HHClient._map_vacancy(payload)

    assert vacancy.id == "12345"
    assert vacancy.title == "Developer"
    assert vacancy.company == ""
    assert vacancy.url is None
    assert vacancy.description == ""
    assert vacancy.contacts is None
