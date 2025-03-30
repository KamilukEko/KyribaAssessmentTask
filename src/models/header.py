class Header:
    def __init__(self, name: str, surname: str, patronymic: str, address: str):
        self.field_id = "01"
        self.name = name
        self.surname = surname
        self.patronymic = patronymic
        self.address = address

    def save_to_string(self) -> str:
        return f"{self.field_id}{self.name:28}{self.surname:30}{self.patronymic:30}{self.address:30}"

    def update(self, **kwargs) -> None:
        valid_fields = {'name', 'surname', 'patronymic', 'address'}
        for field, value in kwargs.items():
            if field not in valid_fields:
                raise ValueError(f"Invalid field: {field}")
            if not isinstance(value, str):
                raise ValueError(f"Field {field} must be a string")
            setattr(self, field, value)

    @staticmethod
    def create_from_string(string) -> 'Header':
        if len(string) != 120:
            raise ValueError("Header must be 120 characters long")

        field_id = string[:2]
        if field_id != "01":
            raise ValueError("Id should be 01")

        return Header(string[2:30].strip(), string[30:60].strip(), string[60:90].strip(), string[90:].strip())

