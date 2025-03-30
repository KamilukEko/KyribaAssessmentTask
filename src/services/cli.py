import argparse
import sys
from decimal import Decimal, ROUND_HALF_UP
from src.models import Transaction
from .file_handler import FileHandler
from .logger import setup_logging

def main():
    parser = argparse.ArgumentParser(description='Fixed-Width File Handler')
    parser.add_argument('file', help='Path to the file')
    parser.add_argument('--logging', action="store_true", help='Print out advanced logging')
    parser.add_argument('--read', action="store_true", help='Read the file')
    parser.add_argument('--add-transaction', nargs=2, metavar=('AMOUNT', 'CURRENCY'),
                        help='Add a transaction (amount currency)')
    parser.add_argument('--update-header', nargs='+', help='Update header (key1 value1 key2 value2)')
    parser.add_argument('--update-transaction', nargs='+',
                        help='Update transaction (counter, field1 value1 field2 value2)')

    args = parser.parse_args()
    logger = setup_logging(args.logging)

    try:
        file_handler = FileHandler(logger, args.file)
        file = file_handler.read_file()

        if args.add_transaction:
            counter = file.get_next_transaction_counter()
            amount = Decimal(args.add_transaction[0]).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            currency = args.add_transaction[1]
            file.add_transaction(Transaction.create_from_string(f"02{str(counter).zfill(6)}{int(amount * 100):012d}{currency:100}"))
            print("Transaction added")
            logger.info("Transaction was added")

        if args.update_header:
            if len(args.update_header) % 2 != 0:
                raise ValueError("Header updates must be key-value pairs")

            header_updates = dict(zip(args.update_header[::2], args.update_header[1::2]))
            file.header.update(**header_updates)
            print("Header updated")
            logger.info("Header was updated")

        if args.update_transaction:
            if len(args.update_transaction) < 3 or len(args.update_transaction) % 2 != 1:
                raise ValueError("Transaction updates must be: counter field1 value1 [field2 value2]")

            counter = int(args.update_transaction[0])
            updates = dict(zip(args.update_transaction[1::2], args.update_transaction[2::2]))

            if not file.update_transaction(counter, **updates):
                print(f"Transaction with counter - {counter} was not found")
                raise ValueError(f"Transaction {counter} not found")

            print("Transaction updated")
            logger.info(f"Transaction {counter} was updated")
            file_handler.save_file(file)

        if args.update_header or args.add_transaction or args.update_transaction:
            file_handler.save_file(file)
            logger.info("Changes saved")

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