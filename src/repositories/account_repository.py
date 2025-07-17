from database import connect_to_mongo
from models import account_model
collection = connect_to_mongo().get_database('api_bank').get_collection('accounts')

def create_account(account_data: account_model.CreateAccount):
    try:
        result = collection.insert_one(account_data.model_dump())
        responseData = account_model.CreateAccountResponse(
            id=str(result.inserted_id)
        )
        return responseData
    except Exception as e:
        print(f"MongoDB error: {e}")
        return None

def get_account_by_account_number(account_number: str):
    try:
        account = collection.find_one({"account_number": account_number}, {"_id": 0})
        if not account:
            return None
        return account
    except Exception as e:
        print(f"MongoDB error: {e}")
        return None