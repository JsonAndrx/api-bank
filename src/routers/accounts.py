from fastapi import APIRouter, HTTPException
from services import account_service
from models import account_model

router = APIRouter()

@router.post("/accounts", response_model=account_model.CreateAccountResponse)
def create_account(account_data: account_model.CreateAccount):
    """
    Crea una nueva cuenta bancaria.
    
    Args:
        account_data (CreateAccount): Datos de la cuenta a crear.
        
    Returns:
        CreateAccountResponse: Respuesta con el ID de la cuenta creada.
        
    Raises:
        HTTPException: 
            - 400 si ya existe una cuenta con el número proporcionado
            - 500 si ocurre un error interno del servidor
    """
    try:
        new_account = account_service.create_account(account_data)
        if new_account is None:
            raise HTTPException(status_code=500, detail="Error creating account in database")
        return new_account
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.patch("/accounts/{account_number}", response_model=account_model.UpdateAccountBalanceResponse)
def update_account_balance(account_data: account_model.UpdateAccountBalance):
    """
    Actualiza el saldo de una cuenta existente.
    
    Args:
        account_data (UpdateAccountBalance): Datos para actualizar el saldo.
        
    Returns:
        UpdateAccountBalanceResponse: Respuesta con el ID y nuevo saldo.
        
    Raises:
        HTTPException:
            - 400 si no se encuentra la cuenta
            - 500 si ocurre un error interno del servidor
    """
    try:
        result = account_service.update_account_balance(account_data)
        if result is None:
            raise HTTPException(status_code=500, detail="Error updating account balance in database")
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/accounts", response_model=account_model.Accounts)
def get_all_accounts():
    """
    Obtiene todas las cuentas bancarias registradas.
    
    Returns:
        Accounts: Lista de todas las cuentas bancarias.
        
    Raises:
        HTTPException: 500 si ocurre un error interno del servidor
    """
    accounts = account_service.get_all_accounts()
    if accounts is None:
        raise HTTPException(status_code=500, detail="Error fetching accounts from database")
    return accounts