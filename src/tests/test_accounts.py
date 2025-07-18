"""
Módulo de pruebas para el servicio de cuentas bancarias.

Este módulo contiene las pruebas unitarias para validar el funcionamiento
correcto del servicio de cuentas (account_service), incluyendo la creación,
actualización y consulta de cuentas bancarias.

Las pruebas utilizan mocks para simular las operaciones de base de datos
y verificar que la lógica de negocio funcione correctamente.
"""

import pytest
from unittest.mock import patch
from services import account_service
from models.account_model import CreateAccount, UpdateAccountBalance, Account, Accounts


@pytest.fixture
def valid_account_data():
    """
    Fixture que proporciona datos válidos para crear una cuenta bancaria.
    
    Returns:
        CreateAccount: Objeto con datos válidos para crear una cuenta de ahorro.
    """
    return CreateAccount(
        account_number="123456789",
        holder_name="John Doe",
        account_type="saving",
        balance=1000.0,
        currency="USD"
    )

@pytest.fixture
def update_account_data():
    """
    Fixture que proporciona datos válidos para actualizar el saldo de una cuenta.
    
    Returns:
        UpdateAccountBalance: Objeto con datos para actualizar el saldo de una cuenta.
    """
    return UpdateAccountBalance(
        id="123456789",
        balance=1500
    )

@pytest.fixture
def valid_get_accounts_data():
    """
    Fixture que proporciona datos de prueba para la consulta de cuentas bancarias.
    
    Returns:
        Accounts: Objeto que contiene una lista de cuentas bancarias de prueba.
    """
    return Accounts(
        accounts=[
            Account(
                id="1",
                account_number="123456789",
                holder_name="John Doe",
                account_type="saving",
                balance=1000.0,
                currency="USD"
            ),
            Account(
                id="2",
                account_number="987654321",
                holder_name="Jane Doe",
                account_type="checking",
                balance=2000.0,
                currency="EUR"
            )
        ]
    )

def test_create_account_success(valid_account_data):
    """
    Prueba que valida la creación exitosa de una cuenta bancaria.
    
    Escenario:
    - No existe una cuenta con el número proporcionado
    - La operación de creación se ejecuta correctamente
    
    Args:
        valid_account_data: Datos válidos para crear una cuenta bancaria
        
    Verifica:
    - Que se retorne el número de cuenta correctamente
    - Que se realice la verificación de duplicados
    - Que se ejecute la creación de la cuenta
    """
    with patch("services.account_service.account_repository.get_account_by_account_number") as mock_get_by_number, \
        patch("services.account_service.account_repository.create_account") as mock_create_account:
        
        mock_get_by_number.return_value = None
        mock_create_account.return_value = "123456789"
        
        result = account_service.create_account(valid_account_data)

        assert result == "123456789"
        mock_get_by_number.assert_called_once_with("123456789")
        mock_create_account.assert_called_once_with(valid_account_data)

def test_create_account_duplicate(valid_account_data):
    """
    Prueba que valida el manejo de error cuando se intenta crear una cuenta duplicada.
    
    Escenario:
    - Ya existe una cuenta con el número proporcionado
    - El sistema debe lanzar una excepción
    
    Args:
        valid_account_data: Datos válidos para crear una cuenta bancaria
        
    Verifica:
    - Que se lance una excepción ValueError con el mensaje correcto
    - Que se verifique la existencia de la cuenta
    - Que NO se ejecute la creación
    """
    with patch("services.account_service.account_repository.get_account_by_account_number") as mock_get_by_number, \
        patch("services.account_service.account_repository.create_account") as mock_create_account:

        mock_get_by_number.return_value = "123456789"

        with pytest.raises(ValueError) as exc_info:
            account_service.create_account(valid_account_data)

        assert str(exc_info.value) == "Account with this account number already exists."
        mock_get_by_number.assert_called_once_with("123456789")
        mock_create_account.assert_not_called()

def test_create_account_db_error(valid_account_data):
    """
    Prueba que valida el manejo de errores de base de datos durante la creación de cuenta.
    
    Escenario:
    - No existe una cuenta duplicada
    - La operación de creación en la base de datos falla
    
    Args:
        valid_account_data: Datos válidos para crear una cuenta bancaria
        
    Verifica:
    - Que se propague la excepción de base de datos
    - Que se verifique la no existencia de duplicados
    - Que se intente la creación de la cuenta
    """
    with patch("services.account_service.account_repository.get_account_by_account_number") as mock_get_by_number, \
        patch("services.account_service.account_repository.create_account") as mock_create_account:
        
        mock_get_by_number.return_value = None
        mock_create_account.side_effect = Exception("DB error")

        with pytest.raises(Exception) as exc_info:
            account_service.create_account(valid_account_data)

        assert str(exc_info.value) == "DB error"
        mock_get_by_number.assert_called_once_with("123456789")
        mock_create_account.assert_called_once_with(valid_account_data)

def test_update_account_balance_success(update_account_data):
    """
    Prueba que valida la actualización exitosa del saldo de una cuenta.
    
    Escenario:
    - Existe una cuenta con el ID proporcionado
    - La operación de actualización se ejecuta correctamente
    
    Args:
        update_account_data: Datos válidos para actualizar el saldo de una cuenta
        
    Verifica:
    - Que se retorne el resultado con el nuevo saldo
    - Que se verifique la existencia de la cuenta
    - Que se ejecute la actualización del saldo
    """
    with patch("services.account_service.account_repository.get_account_by_id") as mock_get_by_id, \
        patch("services.account_service.account_repository.update_balance") as mock_update_balance:

        mock_get_by_id.return_value = {"_id": update_account_data.id, "balance": 1000.0}
        mock_update_balance.return_value = {"id": update_account_data.id, "balance": update_account_data.balance}

        result = account_service.update_account_balance(update_account_data)

        assert result == {
            "id": update_account_data.id,
            "balance": update_account_data.balance
        }

        mock_get_by_id.assert_called_once_with(update_account_data.id)
        mock_update_balance.assert_called_once_with(update_account_data)

def test_update_account_balance_not_found(update_account_data):
    """
    Prueba que valida el manejo de error cuando se intenta actualizar una cuenta inexistente.
    
    Escenario:
    - No existe una cuenta con el ID proporcionado
    - El sistema debe lanzar una excepción
    
    Args:
        update_account_data: Datos para actualizar el saldo de una cuenta
        
    Verifica:
    - Que se lance una excepción ValueError con el mensaje correcto
    - Que se verifique la inexistencia de la cuenta
    - Que NO se ejecute la actualización del saldo
    """
    with patch("services.account_service.account_repository.get_account_by_id") as mock_get_by_id:
        mock_get_by_id.return_value = None

        with pytest.raises(ValueError) as exc_info:
            account_service.update_account_balance(update_account_data)

        assert str(exc_info.value) == "Account not found."
        mock_get_by_id.assert_called_once_with(update_account_data.id)

def test_update_account_balance_db_error(update_account_data):
    """
    Prueba que valida el manejo de errores de base de datos durante la actualización de saldo.
    
    Escenario:
    - Existe una cuenta con el ID proporcionado
    - La operación de actualización en la base de datos falla
    
    Args:
        update_account_data: Datos para actualizar el saldo de una cuenta
        
    Verifica:
    - Que se propague la excepción de base de datos
    - Que se verifique la existencia de la cuenta
    - Que se intente la actualización del saldo
    """
    with patch("services.account_service.account_repository.get_account_by_id") as mock_get_by_id, \
        patch("services.account_service.account_repository.update_balance") as mock_update_balance:

        mock_get_by_id.return_value = {"_id": update_account_data.id, "balance": 1000.0}

        mock_update_balance.side_effect = Exception("DB error")

        with pytest.raises(Exception) as exc_info:
            account_service.update_account_balance(update_account_data)

        assert str(exc_info.value) == "DB error"
        mock_get_by_id.assert_called_once_with(update_account_data.id)
        mock_update_balance.assert_called_once_with(update_account_data)

def test_get_all_accounts(valid_get_accounts_data):
    """
    Prueba que valida la consulta exitosa de todas las cuentas bancarias.
    
    Escenario:
    - Se obtienen todas las cuentas de la base de datos
    - La operación se ejecuta correctamente
    
    Args:
        valid_get_accounts_data: Datos de prueba que simulan la respuesta de la base de datos
        
    Verifica:
    - Que se retorne el número correcto de cuentas
    - Que las cuentas tengan los IDs esperados
    - Que se ejecute la consulta a la base de datos
    """
    with patch("services.account_service.account_repository.get_all_accounts") as mock_get_all:
        mock_get_all.return_value = valid_get_accounts_data

        result = account_service.get_all_accounts()

        assert len(result.accounts) == 2
        assert result.accounts[0].id == "1"
        assert result.accounts[1].id == "2"
        mock_get_all.assert_called_once()
