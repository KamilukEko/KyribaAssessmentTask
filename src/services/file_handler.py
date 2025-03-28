from src.models import Header, Transaction, Footer
from src.models.file import File


class FileHandler:
    def __init__(self, logger, file_path):
        self.logger = logger
        self.file_path = file_path

    def read_file(self) -> File:
        self.logger.info(f"Reading file {self.file_path}")
        try:
            with open(self.file_path, "r") as file:
                content = file.readlines()

            if not content:
                raise ValueError("File is empty")

            self.logger.info("Reading header")
            header = Header.create_from_string(content[0].rstrip('\n'))

            transactions = []
            for index, line in enumerate(content[1:-1]):
                self.logger.info("Reading transaction %d", index)
                transactions.append(Transaction.create_from_string(line.rstrip('\n')))


            self.logger.info("Reading footer")
            footer = Footer.create_from_string(content[-1].rstrip('\n'))

            if len(transactions) != footer.total_counter:
                raise ValueError("Number of transactions doesn't match header count")

            if footer.control_sum != sum(transaction.amount for transaction in transactions):
                raise ValueError("Control sum doesn't match sum of transactions")

            self.logger.info("File was read successfully")
            return File(header, transactions, footer)
        except Exception as e:
            self.logger.error(f"Error reading file: {str(e)}")
            raise

    def save_file(self, file: File) -> None:
        self.logger.info(f"Saving file to {self.file_path}")
        try:
            with open(self.file_path, "w") as f:
                f.write(file.header.save_to_string() + "\n")

                for transaction in file.transactions:
                    f.write(transaction.save_to_string() + "\n")

                f.write(file.footer.save_to_string())

            self.logger.info("File was saved successfully")
        except Exception as e:
            self.logger.error(f"Error saving file: {str(e)}")
            raise
