import pytest
from unittest.mock import Mock, mock_open, patch
from src.services.file_handler import FileHandler
from src.models import File

@pytest.fixture
def file_handler():
    logger = Mock()
    return FileHandler(logger, 'test.txt')

valid_files = [
    ([
        "01" + "Kamil" + " " * 23 + "Pracki" + " " * 24 + "Krzysztof" + " " * 21 + "Noworusynowska 161c" + " " * 11 + "\n",
        "02" + "000123" + "000012345678" + "EUR" + " " * 97 + "\n",
        "02" + "000124" + "000123345278" + "PLN" + " " * 97 + "\n",
        "03" + "000002" + "000135690956" + " " * 100,
    ], 2, 1356909.56)
]

@pytest.mark.parametrize("file_content, count, control_sum", valid_files)
def test_read_file_success(file_handler: FileHandler, file_content: [str], count, control_sum):
    with patch('builtins.open', mock_open(read_data=''.join(file_content))):
        result = file_handler.read_file()

        assert isinstance(result, File)
        assert result.footer.total_counter == count
        assert result.footer.control_sum == control_sum

def test_read_empty_file(file_handler):
    with patch('builtins.open', mock_open(read_data='')):
        with pytest.raises(ValueError, match="File is empty"):
            file_handler.read_file()
