import pytest
from src.models import Footer
from decimal import Decimal

footer_valid_test_data = [
    (
        "03" + "000002" + "000000123456" + " " * 100,
        Footer(2, Decimal('1234.56'))
    ),
    (
        "03" + "000100" + "000050000000" + " " * 100,
        Footer(100, Decimal('500000.00'))
    ),
]

footer_invalid_test_data = [
    "02" + "000002" + "000000123456" + " " * 100,
    "03" + "00002" + "000000123456" + " " * 100,
    "03" + "000002" + "000000123456" + " " * 101,
    "",
]

@pytest.mark.parametrize("input_str, expected_footer", footer_valid_test_data)
def test_footer_create_from_string_converts(input_str: str, expected_footer: Footer):
    result = Footer.create_from_string(input_str)

    assert result.total_counter == expected_footer.total_counter
    assert result.control_sum == expected_footer.control_sum
    assert result.field_id == expected_footer.field_id

@pytest.mark.parametrize("expected_string, footer", footer_valid_test_data)
def test_footer_save_to_string_converts(footer: Footer, expected_string: str):
    assert footer.save_to_string() == expected_string

@pytest.mark.parametrize("input_str", footer_invalid_test_data)
def test_footer_create_from_string_fails(input_str: str):
    with pytest.raises((ValueError, IndexError)):
        Footer.create_from_string(input_str)