import argparse
import sys
from decimal import Decimal, ROUND_HALF_UP
from src.models import Transaction
from .file_handler import FileHandler
from .logger import setup_logging

def main():
    parser = argparse.ArgumentParser(description='Fixed-Width File Handler')
    parser.add_argument('file', help='Path to the file')
    parser.add_argument('--read', action="store_true", help='Read the file')
    parser.add_argument('--add-transaction', nargs=2, metavar=('AMOUNT', 'CURRENCY'),
                        help='Add a transaction (amount currency)')

    args = parser.parse_args()
    logger = setup_logging()

    try:
        file_handler = FileHandler(logger, args.file)
        file = file_handler.read_file()

        if args.add_transaction:
            counter = file.get_next_transaction_counter()
            amount = Decimal(args.add_transaction[0]).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            currency = args.add_transaction[1]
            file.add_transaction(Transaction.create_from_string(f"02{str(counter).zfill(6)}{int(amount * 100):012d}{currency:100}"))
            file_handler.save_file(file)

        if args.read:
            print(file)
            logger.info("File content was displayed")
            return



    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)

    finally:
        logger.info("Script execution finished")


if __name__ == '__main__':
    main()