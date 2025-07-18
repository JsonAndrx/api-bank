from database import connect_to_mongo
from models import account_model
from bson import ObjectId

collection = connect_to_mongo().get_database('api_bank').get_collection('accounts')

def create_account(account_data: account_model.CreateAccount):
    """
    Crea una nueva cuenta bancaria en la base de datos.
    
    Args:
        account_data (CreateAccount): Datos de la cuenta a crear.
        
    Returns:
        CreateAccountResponse: Respuesta con el ID de la cuenta creada.
        None: Si ocurre un error durante la creación.
    """
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
    """
    Busca una cuenta por su número de cuenta.
    
    Args:
        account_number (str): Número de cuenta a buscar.
        
    Returns:
        dict: Datos de la cuenta encontrada.
        None: Si no se encuentra la cuenta o ocurre un error.
    """
    try:
        account = collection.find_one({"account_number": account_number}, {"_id": 0})
        if not account:
            return None
        return account
    except Exception as e:
        print(f"MongoDB error: {e}")
        return None

def update_balance(account_data: account_model.UpdateAccountBalance):
    """
    Actualiza el saldo de una cuenta existente.
    
    Args:
        account_data (UpdateAccountBalance): Datos para actualizar el saldo.
        
    Returns:
        dict: Diccionario con id y balance actualizado.
        None: Si no se encuentra la cuenta o ocurre un error.
    """
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
    """
    Busca una cuenta por su ID único.
    
    Args:
        account_id (str): ID de la cuenta a buscar.
        
    Returns:
        dict: Datos de la cuenta encontrada.
        None: Si no se encuentra la cuenta o ocurre un error.
    """
    try:
        account = collection.find_one({"_id": ObjectId(account_id)}, {"_id": 0})
        if not account:
            return None
        return account
    except Exception as e:
        print(f"MongoDB error: {e}")
        return None
    
def get_all_accounts():
    """
    Obtiene todas las cuentas bancarias registradas.
    
    Returns:
        Accounts: Objeto que contiene la lista de todas las cuentas.
        None: Si ocurre un error durante la consulta.
    """
    try:
        raw_accounts = collection.find({})
        accounts = []
        for acc in raw_accounts:
            acc["id"] = str(acc["_id"])
            del acc["_id"]
            accounts.append(acc)
        
        data = account_model.Accounts.model_validate({"accounts": accounts})
        return data
    except Exception as e:
        print(f"MongoDB error: {e}")
        return None