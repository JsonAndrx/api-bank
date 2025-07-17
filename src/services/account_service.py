from repositories import account_repository
from models import account_model

def create_account(account_data: account_model.CreateAccount):
    if account_repository.get_account_by_account_number(account_data.account_number):
        raise ValueError("Account with this account number already exists.")
    account = account_repository.create_account(account_data)
    return account
