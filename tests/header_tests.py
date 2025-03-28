import pytest
from src.models import Header

header_valid_test_data = [
    (
        "01" + "John" + " " * 24 + "Smith" + " " * 25 + "Mark" + " " * 26 + "123 Main St" + " " * 19,
        Header("John", "Smith", "Mark", "123 Main St")
    ),
    (
        "01" + "Kamil" + " " * 23 + "Pracki" + " " * 24 + "Krzysztof" + " " * 21 + "Noworusynowska 161c" + " " * 11,
        Header("Kamil", "Pracki", "Krzysztof", "Noworusynowska 161c")
    ),
]

header_invalid_test_data = [
    "02" + "Kamil" + " " * 23 + "Pracki" + " " * 24 + "Krzysztof" + " " * 21 + "Noworusynowska 161c" + " " * 11,
    "01" + "Kamil" + " " * 23 + "Pracki" + " " * 53 + "Krzysztof" + " " * 21 + "Noworusynowska 161c" + " " * 11,
    "",
]

@pytest.mark.parametrize("input_str, expected_header", header_valid_test_data)
def test_header_create_from_string_converts(input_str: str, expected_header: Header):
    result = Header.create_from_string(input_str)

    assert result.name.strip() == expected_header.name
    assert result.surname.strip() == expected_header.surname
    assert result.patronymic.strip() == expected_header.patronymic
    assert result.address.strip() == expected_header.address
    assert result.field_id == expected_header.field_id

@pytest.mark.parametrize("expected_string, header", header_valid_test_data)
def test_header_create_from_string_converts(header: Header, expected_string: str):
    assert header.save_to_string() == expected_string

@pytest.mark.parametrize("input_str", header_invalid_test_data)
def test_header_create_from_string_fails(input_str: str):
    with pytest.raises((ValueError, IndexError)):
        Header.create_from_string(input_str)
