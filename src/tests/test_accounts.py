import pytest
from unittest.mock import patch
from services import account_service
from models.account_model import CreateAccount


@pytest.fixture
def valid_account_data():
    return CreateAccount(
        account_number="123456789",
        holder_name="John Doe",
        account_type="saving",
        initial_balance=1000.0,
        currency="USD"
    )

def test_create_account_success(valid_account_data):
    with patch("services.account_service.account_repository.get_account_by_account_number") as mock_get_by_number, \
        patch("services.account_service.account_repository.create_account") as mock_create_account:
        
        mock_get_by_number.return_value = None
        mock_create_account.return_value = "123456789"
        
        result = account_service.create_account(valid_account_data)

        assert result == "123456789"
        mock_get_by_number.assert_called_once_with("123456789")
        mock_create_account.assert_called_once_with(valid_account_data)

def test_create_account_duplicate(valid_account_data):
    with patch("services.account_service.account_repository.get_account_by_account_number") as mock_get_by_number, \
        patch("services.account_service.account_repository.create_account") as mock_create_account:

        mock_get_by_number.return_value = "123456789"

        with pytest.raises(ValueError) as exc_info:
            account_service.create_account(valid_account_data)

        assert str(exc_info.value) == "Account with this account number already exists."
        mock_get_by_number.assert_called_once_with("123456789")
        mock_create_account.assert_not_called()

def test_create_account_db_error(valid_account_data):
    with patch("services.account_service.account_repository.get_account_by_account_number") as mock_get_by_number, \
        patch("services.account_service.account_repository.create_account") as mock_create_account:
        
        mock_get_by_number.return_value = None
        mock_create_account.side_effect = Exception("DB error")

        with pytest.raises(Exception) as exc_info:
            account_service.create_account(valid_account_data)

        assert str(exc_info.value) == "DB error"
        mock_get_by_number.assert_called_once_with("123456789")
        mock_create_account.assert_called_once_with(valid_account_data)