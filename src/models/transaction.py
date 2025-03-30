from .currency import Currency
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation


class Transaction:
    def __init__(self, counter: int, amount: Decimal, currency: Currency):
        self.field_id = "02"
        self.counter = counter
        self.amount = amount
        self.currency = currency

    def save_to_string(self) -> str:
        return f"{self.field_id}{str(self.counter).zfill(6)}{int(self.amount * 100):012d}{self.currency.value:100}"

    def update(self, **kwargs) -> Decimal:
        valid_fields = {'amount', 'currency'}
        old_amount = self.amount

        for field, value in kwargs.items():
            if field not in valid_fields:
                raise ValueError(f"Invalid field: {field}")

            if field == 'amount':
                if not isinstance(value, (str, Decimal)):
                    raise ValueError("Amount must be a string or Decimal")
                try:
                    self.amount = Decimal(value).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                except (InvalidOperation, ValueError):
                    raise ValueError("Invalid literal for Decimal")
            elif field == 'currency':
                if not isinstance(value, (str, Currency)):
                    raise ValueError("Currency must be a string or Currency enum")
                self.currency = Transaction.get_currency(value)

        return self.amount - old_amount

    @staticmethod
    def get_currency(currency_str) -> Currency:
        try:
            return Currency(currency_str)
        except ValueError:
            raise ValueError(f"Invalid currency")

    @staticmethod
    def create_from_string(string) -> 'Transaction':
        if len(string) != 120:
            raise ValueError("Transaction must be 120 characters long")

        field_id = string[:2]
        if field_id != "02":
            raise ValueError("Id should be 02")

        try:
            counter = int(string[2:8])
        except ValueError:
            raise ValueError("Invalid counter format")

        amount_str = string[8:20]
        if not amount_str.isdigit():
            raise ValueError("Invalid amount format")

        try:
            amount = Decimal(amount_str) / Decimal('100')
        except (InvalidOperation, ValueError):
            raise ValueError("Invalid amount format")

        currency = Transaction.get_currency(string[20:23])

        return Transaction(counter, amount, currency)
