from src.models import Header, Transaction, Footer

class File:
    def __init__(self, header: Header, transactions: [Transaction], footer: Footer):
        self.header = header
        self.transactions = transactions
        self.footer = footer

    def get_next_transaction_counter(self) -> int:
        return max(transaction.counter for transaction in self.transactions) + 1

    def update_transaction(self, counter: int, **kwargs) -> bool:
        for transaction in self.transactions:
            if transaction.counter == counter:
                amount_change = transaction.update(**kwargs)
                if not amount_change:
                    return False
                self.footer.control_sum += amount_change
                return True
        return False

    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)
        self.footer.total_counter += 1
        self.footer.control_sum += transaction.amount

    def __str__(self) -> str:
        lines = [
            "File",
            "├── Header",
            f"│   ├── name: \"{self.header.name}\"",
            f"│   ├── surname: \"{self.header.surname}\"",
            f"│   ├── patronymic: \"{self.header.patronymic}\"",
            f"│   └── address: \"{self.header.address}\"",
            "│",
            "├── Transactions[]"
        ]

        for i, tx in enumerate(self.transactions, 1):
            lines.extend([
                "│   " + ("└── " if i == len(self.transactions) else "├── ") + f"Transaction {i}",
                "│   │   ├── counter: " + str(tx.counter),
                "│   │   ├── amount: " + str(tx.amount),
                "│   │   └── currency: " + str(tx.currency.name),
                "│   │" if i < len(self.transactions) else "│"
            ])

        lines.extend([
            "└── Footer",
            f"    ├── total_counter: {self.footer.total_counter}",
            f"    └── control_sum: {self.footer.control_sum}"
        ])

        return "\n".join(lines)