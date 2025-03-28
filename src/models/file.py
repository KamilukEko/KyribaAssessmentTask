from src.models import Header, Transaction, Footer

class File:
    def __init__(self, header: Header, transactions: [Transaction], footer: Footer):
        self.header = header
        self.transactions = transactions
        self.footer = footer