from repositories import account_repository
from models import account_model

def create_account(account_data: account_model.CreateAccount):
    if account_repository.get_account_by_account_number(account_data.account_number):
        raise ValueError("Account with this account number already exists.")
    account = account_repository.create_account(account_data)
    return account

def update_account_balance(account_data: account_model.UpdateAccountBalance):
    if not account_repository.get_account_by_id(account_data.id):
        raise ValueError("Account not found.")
    result = account_repository.update_balance(account_data)
    return result

def get_all_accounts():
    accounts = account_repository.get_all_accounts()
    return accounts
