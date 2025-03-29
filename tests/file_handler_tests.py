import pytest
from unittest.mock import Mock, mock_open, patch, call
from src.services.file_handler import FileHandler
from src.models import Header, Transaction, Footer, File, Currency

@pytest.fixture
def file_handler():
    logger = Mock()
    return FileHandler(logger, 'test.txt')

valid_files = [
    ([
        "01" + "Kamil" + " " * 23 + "Pracki" + " " * 24 + "Krzysztof" + " " * 21 + "Noworusynowska 161c" + " " * 11 + '\n',
        "02" + "000123" + "000012345678" + "EUR" + " " * 97 + '\n',
        "02" + "000124" + "000123345278" + "PLN" + " " * 97 + '\n',
        "03" + "000002" + "000135690956" + " " * 100,
    ], File(
        Header("Kamil", "Pracki", "Krzysztof", "Noworusynowska 161c"),
        [
            Transaction(123, 123456.78, Currency.EUR),
            Transaction(124, 1233452.78, Currency.PLN),
        ],
        Footer(2, 1356909.56)
    ))
]
invalid_files = [
    ([
         "01" + "Kamil" + " " * 23 + "Pracki" + " " * 24 + "Krzysztof" + " " * 21 + "Noworusynowska 161c" + " " * 11,
         "02" + "000123" + "00001234ABCD" + "EUR" + " " * 97,
         "02" + "000124" + "000123345278" + "PLN" + " " * 97,
         "03" + "000002" + "000135690956" + " " * 100
     ], "Invalid amount format"),
    ([
         "01" + "Kamil" + " " * 23 + "Pracki" + " " * 24 + "Krzysztof" + " " * 21 + "Noworusynowska 161c" + " " * 11,
         "02" + "000123" + "000012345678" + "EUR" + " " * 97,
         "02" + "000124" + "000123345278" + "PLN" + " " * 97,
         "03" + "000002" + "000999999999" + " " * 100
     ], "Control sum doesn't match sum of transactions"),
    ([
         "01" + "Kamil" + " " * 23 + "Pracki" + " " * 24 + "Krzysztof" + " " * 21 + "Noworusynowska 161c" + " " * 11,
         "02" + "000123" + "000012345678" + "EUR" + " " * 97,
         "02" + "000124" + "000123345278" + "PLN" + " " * 97,
         "03" + "000003" + "000135690956" + " " * 100
     ], "Number of transactions doesn't match header count"),
    ([
         "01" + "Kamil" + " " * 23 + "Pracki" + " " * 24 + "Krzysztof" + " " * 21 + "Noworusynowska 161c" + " " * 11,
         "02" + "000123" + "000012345678" + "EUR" + " " * 97,
         "02" + "00A124" + "000123345278" + "PLN" + " " * 97,
         "03" + "000002" + "000135690956" + " " * 100,
    ], "Invalid counter format")
]

@pytest.mark.parametrize("file_content, expected_object", valid_files)
def test_read_file_success(file_handler: FileHandler, file_content: [str], expected_object: File):
    with patch('builtins.open', mock_open(read_data=''.join(file_content))):
        result = file_handler.read_file()

        assert isinstance(result, File)

        assert result.header.name == expected_object.header.name
        assert result.header.surname== expected_object.header.surname
        assert result.header.patronymic == expected_object.header.patronymic
        assert result.header.address == expected_object.header.address

        assert len(result.transactions) == len(expected_object.transactions)
        for res_trans, exp_trans in zip(result.transactions, expected_object.transactions):
            assert res_trans.counter == exp_trans.counter
            assert res_trans.amount == exp_trans.amount
            assert res_trans.currency == exp_trans.currency

        assert result.footer.total_counter == expected_object.footer.total_counter
        assert result.footer.control_sum == expected_object.footer.control_sum

@pytest.mark.parametrize("file_content, expected_object", valid_files)
def test_save_file_success(file_handler: FileHandler, file_content: [str], expected_object: File):
    mock_file = mock_open()
    with patch('builtins.open', mock_file):
        file_handler.save_file(expected_object)

        mock_file.assert_called_once_with(file_handler.file_path, 'w')
        handle = mock_file()

        calls = [call(line) for line in file_content]
        handle.write.assert_has_calls(calls)

@pytest.mark.parametrize("file_content, error_message", invalid_files)
def test_read_file_errors(file_handler: FileHandler, file_content: [str], error_message: str):
    with patch('builtins.open', mock_open(read_data='\n'.join(file_content))):
        with pytest.raises(ValueError, match=error_message):
            file_handler.read_file()

def test_read_empty_file(file_handler):
    with patch('builtins.open', mock_open(read_data='')):
        with pytest.raises(ValueError, match="File is empty"):
            file_handler.read_file()
