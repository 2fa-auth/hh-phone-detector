from app.phones.extractor import extract_valid_phones


def test_phone_from_description():
    result = extract_valid_phones(
        "Звоните +7 (999) 123-45-67",
        None,
    )
    assert len(result) == 1
    assert result[0][0].normalized == "+79991234567"
    assert result[0][1] == "description"


def test_phone_from_contacts():
    contacts = {
        "phones": [
            {"value": "+7 916 555 44 33"}
        ]
    }
    result = extract_valid_phones("", contacts)

    assert len(result) == 1
    assert result[0][0].normalized == "+79165554433"
    assert result[0][1] == "contacts"


def test_duplicate_is_removed():
    contacts = {"phones": [{"value": "8 (999) 123-45-67"}]}
    result = extract_valid_phones(
        "Телефон +7 999 123-45-67",
        contacts,
    )

    assert len(result) == 1
    assert result[0][1] == "contacts"


def test_numbers_are_not_automatically_phones():
    result = extract_valid_phones(
        "ID 123456789, зарплата 150000, код 123456",
        None,
    )
    assert result == []


def test_multiple_phones():
    result = extract_valid_phones(
        "Звоните +7 999 123-45-67 или +7 916 555-44-33",
        None,
    )
    assert {phone.normalized for phone, _ in result} == {
        "+79991234567",
        "+79165554433",
    }
