import pytest
from decimal import Decimal
from src.models import File, Header, Transaction, Footer, Currency
from src.services import FileHandler, setup_logging


@pytest.fixture
def sample_file():
    header = Header("John", "Doe", "Smith", "123 Main St")
    transactions = [
        Transaction(1, Decimal('100.00'), Currency.EUR),
        Transaction(2, Decimal('200.00'), Currency.USD)
    ]
    footer = Footer(2, Decimal('300.00'))
    return File(header, transactions, footer)


@pytest.mark.parametrize("field_updates, expected_values", [
    ({"name": "Jane"}, {"name": "Jane", "surname": "Doe"}),
    ({"surname": "Smith", "address": "456 Oak St"}, {"surname": "Smith", "address": "456 Oak St"}),
])
def test_update_header(sample_file, field_updates, expected_values):
    sample_file.header.update(**field_updates)
    for field, value in expected_values.items():
        assert getattr(sample_file.header, field) == value


@pytest.mark.parametrize("invalid_field", [
    "invalid_field",
    "phone",
    "email"
])
def test_update_header_invalid(sample_file, invalid_field):
    with pytest.raises(ValueError, match="Invalid field"):
        sample_file.header.update(**{invalid_field: "value"})


@pytest.mark.parametrize("counter, updates, expected_values", [
    (1, {"amount": "150.00"}, {"amount": Decimal("150.00"), "control_sum": Decimal("350.00")}),
    (2, {"currency": "EUR"}, {"currency": Currency.EUR, "control_sum": Decimal("300.00")}),
])
def test_update_transaction(sample_file, counter, updates, expected_values):
    success = sample_file.update_transaction(counter, **updates)
    assert success is True

    transaction = next(t for t in sample_file.transactions if t.counter == counter)
    for field, value in expected_values.items():
        if field == "control_sum":
            assert sample_file.footer.control_sum == value
        else:
            assert getattr(transaction, field) == value


@pytest.mark.parametrize("counter, field, invalid_value, error_message", [
    (1, "amount", 123, "Amount must be a string or Decimal"),
    (1, "currency", 123, "Currency must be a string or Currency enum"),
    (1, "amount", "invalid", "Invalid literal for Decimal"),
    (1, "currency", "INVALID", "Invalid currency"),
])
def test_transaction_validation(sample_file, counter, field, invalid_value, error_message):
    with pytest.raises(ValueError, match=error_message):
        sample_file.update_transaction(counter, **{field: invalid_value})
