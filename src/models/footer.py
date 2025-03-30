from decimal import Decimal

class Footer:
    def __init__(self, total_counter: int, control_sum: Decimal):
        self.field_id = "03"
        self.total_counter = total_counter
        self.control_sum = control_sum

    def save_to_string(self) -> str:
        return f"{self.field_id}{str(self.total_counter).zfill(6)}{int(self.control_sum * 100):012d}{' ' * 100}"

    @staticmethod
    def create_from_string(string) -> 'Footer':
        if len(string) != 120:
            raise ValueError("Transaction must be 120 characters long")

        field_id = string[:2]
        if field_id != "03":
            raise ValueError("Id should be 03")

        control_sum_str = string[8:20]
        if not control_sum_str.isdigit():
            raise ValueError("Invalid amount format")

        try:
            control_sum = Decimal(control_sum_str) / Decimal('100')
        except (InvalidOperation, ValueError):
            raise ValueError("Invalid amount format")

        return Footer(int(string[2:8]), control_sum)
