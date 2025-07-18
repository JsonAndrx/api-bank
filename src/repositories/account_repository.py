from database import connect_to_mongo
from models import account_model
from bson import ObjectId

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

def update_balance(account_data: account_model.UpdateAccountBalance):
    try:
        result = collection.update_one(
            {"_id": ObjectId(account_data.id)},
            {"$inc": {"balance": account_data.balance}}
        )

        if result.modified_count == 0:
            return None

        updated_account = collection.find_one(
            {"_id": ObjectId(account_data.id)},
            {"_id": 1, "balance": 1}
        )

        if not updated_account:
            return None

        return {
            "id": str(updated_account["_id"]),
            "balance": updated_account["balance"]
        }

    except Exception as e:
        print(f"MongoDB error: {e}")
        return None
    
def get_account_by_id(account_id: str):
    try:
        account = collection.find_one({"_id": ObjectId(account_id)}, {"_id": 0})
        if not account:
            return None
        return account
    except Exception as e:
        print(f"MongoDB error: {e}")
        return None