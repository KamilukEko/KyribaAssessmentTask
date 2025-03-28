import pytest
from src.models import Transaction
from src.models.currency import Currency

transaction_valid_test_data = [
    (
        "02" + "000001" + "000000100000" + "USD" + " " * 97,
        Transaction(1, 1000.00, Currency.USD)
    ),
    (
        "02" + "000123" + "000012345678" + "EUR" + " " * 97,
        Transaction(123, 123456.78, Currency.EUR)
    ),
]

transaction_invalid_test_data = [
    "01" + "000001" + "000000100000" + "USD" + " " * 96,
    "02" + "00001" + "000000100000" + "USD" + " " * 97,
    "02" + "000001" + "00000010000" + "USD" + " " * 97,
    "02" + "000001" + "000000100000" + "XXX" + " " * 96,
    "",
]

@pytest.mark.parametrize("input_str, expected_transaction", transaction_valid_test_data)
def test_transaction_create_from_string_converts(input_str: str, expected_transaction: Transaction):
    result = Transaction.create_from_string(input_str)

    assert result.counter == expected_transaction.counter
    assert result.amount == expected_transaction.amount
    assert result.currency == expected_transaction.currency
    assert result.field_id == expected_transaction.field_id

@pytest.mark.parametrize("expected_string, transaction", transaction_valid_test_data)
def test_transaction_save_to_string_converts(transaction: Transaction, expected_string: str):
    assert transaction.save_to_string() == expected_string

@pytest.mark.parametrize("input_str", transaction_invalid_test_data)
def test_transaction_create_from_string_fails(input_str: str):
    with pytest.raises((ValueError, IndexError)):
        Transaction.create_from_string(input_str)