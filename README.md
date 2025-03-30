## Installation

```bash
pip install -r requirements.txt
```

## Example commands usage

### Read file
Read file content:
```bash
python main.py example_transaction.txt --read
```

### Add transaction
Add a new transaction to existing file:
```bash
python main.py example_transaction.txt --add-transaction 100.00 EUR
```

### Update transaction
Update an existing transaction:
```bash
python main.py example_transaction.txt --update-transaction 123 amount 150.50 currency USD
```

### Update header
Update header:
```bash
python main.py example_transaction.txt --update-header name "Jack"
```

### Logging
Prints out more information during runtime:
```bash
python main.py example_transaction.txt --read --logging
```

## Notes

- Amounts are stored with 2 decimal places
- Supported currencies: EUR, USD, GBP
- Logs are written to `logs/transactions_manager.log`
