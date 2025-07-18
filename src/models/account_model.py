from pydantic import BaseModel, Field
from typing import Literal

class CreateAccount(BaseModel):
    """
    Modelo para crear una nueva cuenta bancaria.
    
    Attributes:
        account_number (str): Número único de la cuenta (5-20 caracteres).
        holder_name (str): Nombre del titular de la cuenta (máximo 100 caracteres).
        account_type (Literal): Tipo de cuenta, puede ser "saving" o "checking".
        balance (float): Saldo inicial de la cuenta.
        currency (Literal): Moneda de la cuenta, puede ser "USD" o "EUR".
    """
    account_number: str = Field(max_length=20, min_length=5)
    holder_name: str = Field(max_length=100)
    account_type: Literal["saving", "checking"]
    balance: float
    currency: Literal["USD", "EUR"]

class CreateAccountResponse(BaseModel):
    """
    Modelo de respuesta para la creación de una cuenta bancaria.
    
    Attributes:
        id (str): ID único generado para la cuenta creada.
    """
    id: str 


class UpdateAccountBalance(BaseModel):
    """
    Modelo para actualizar el saldo de una cuenta existente.
    
    Attributes:
        id (str): ID único de la cuenta a actualizar.
        balance (float): Nuevo saldo de la cuenta (debe ser >= 1).
    """
    id: str
    balance: float = Field(..., ge=1)

class UpdateAccountBalanceResponse(BaseModel):
    """
    Modelo de respuesta para la actualización del saldo de una cuenta.
    
    Attributes:
        id (str): ID de la cuenta actualizada.
        balance (float): Nuevo saldo de la cuenta.
    """
    id: str
    balance: float

class Account(BaseModel):
    """
    Modelo completo de una cuenta bancaria.
    
    Attributes:
        id (str): ID único de la cuenta.
        account_number (str): Número de la cuenta.
        holder_name (str): Nombre del titular.
        account_type (str): Tipo de cuenta.
        balance (float): Saldo actual de la cuenta.
        currency (str): Moneda de la cuenta.
    """
    id: str
    account_number: str
    holder_name: str
    account_type: str
    balance: float
    currency: str

class Accounts(BaseModel):
    """
    Modelo para una colección de cuentas bancarias.
    
    Attributes:
        accounts (list[Account]): Lista de cuentas bancarias.
    """
    accounts: list[Account]