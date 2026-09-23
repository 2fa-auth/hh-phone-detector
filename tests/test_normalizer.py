from app.phones.normalizer import normalize_phone


def test_russian_phone_with_plus():
    result = normalize_phone("+7 (999) 123-45-67")
    assert result is not None
    assert result.normalized == "+79991234567"


def test_russian_phone_with_eight():
    result = normalize_phone("8 (999) 123-45-67")
    assert result is not None
    assert result.normalized == "+79991234567"


def test_international_phone():
    result = normalize_phone("+49 151 23456789")
    assert result is not None
    assert result.normalized == "+4915123456789"


def test_invalid_phone():
    assert normalize_phone("123456") is None
