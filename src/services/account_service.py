from repositories import account_repository
from models import account_model

def create_account(account_data: account_model.CreateAccount):
    """
    Crea una nueva cuenta bancaria con validaciones de negocio.
    
    Args:
        account_data (CreateAccount): Datos de la cuenta a crear.
        
    Returns:
        CreateAccountResponse: Respuesta con el ID de la cuenta creada.
        
    Raises:
        ValueError: Si ya existe una cuenta con el número proporcionado.
    """
    # Validar que no exista una cuenta con el mismo número
    if account_repository.get_account_by_account_number(account_data.account_number):
        raise ValueError("Account with this account number already exists.")
    account = account_repository.create_account(account_data)
    return account

def update_account_balance(account_data: account_model.UpdateAccountBalance):
    """
    Actualiza el saldo de una cuenta existente.
    
    Args:
        account_data (UpdateAccountBalance): Datos para actualizar el saldo.
        
    Returns:
        dict: Diccionario con id y balance actualizado.
        
    Raises:
        ValueError: Si no se encuentra la cuenta con el ID proporcionado.
    """
    # Validar que la cuenta existe
    if not account_repository.get_account_by_id(account_data.id):
        raise ValueError("Account not found.")
    result = account_repository.update_balance(account_data)
    return result

def get_all_accounts():
    """
    Obtiene todas las cuentas bancarias registradas.
    
    Returns:
        Accounts: Objeto que contiene la lista de todas las cuentas.
    """
    accounts = account_repository.get_all_accounts()
    return accounts
