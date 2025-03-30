from .currency import Currency
from decimal import Decimal


class Transaction:
    def __init__(self, counter: int, amount: Decimal, currency: Currency):
        self.field_id = "02"
        self.counter = counter
        self.amount = amount
        self.currency = currency

    def save_to_string(self) -> str:
        return f"{self.field_id}{str(self.counter).zfill(6)}{int(self.amount * 100):012d}{self.currency.value:100}"

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
        except ValueError:
            raise ValueError("Invalid amount format")

        try:
            currency = Currency(string[20:23])
        except ValueError:
            raise ValueError(f"Invalid currency")


        return Transaction(counter, amount, currency)
