from fastapi import APIRouter, HTTPException
from services import account_service
from models import account_model

router = APIRouter()

@router.post("/accounts", response_model=account_model.CreateAccountResponse)
def create_account(account_data: account_model.CreateAccount):
    try:
        new_account = account_service.create_account(account_data)
        if new_account is None:
            raise HTTPException(status_code=500, detail="Error creating account in database")
        return new_account
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.patch("/accounts/{account_number}", response_model=account_model.UpdateAccountBalanceResponse)
def update_account_balance( account_data: account_model.UpdateAccountBalance):
    try:
        result = account_service.update_account_balance(account_data)
        if result is None:
            raise HTTPException(status_code=500, detail="Error updating account balance in database")
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))