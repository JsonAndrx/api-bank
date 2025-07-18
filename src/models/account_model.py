from pydantic import BaseModel, Field
from typing import Literal

class CreateAccount(BaseModel):
    account_number: str = Field(max_length=20, min_length=5)
    holder_name: str = Field(max_length=100)
    account_type: Literal["saving", "checking"]
    balance: float
    currency: Literal["USD", "EUR"]

class CreateAccountResponse(BaseModel):
    id: str 


class UpdateAccountBalance(BaseModel):
    id: str
    balance: float = Field(..., ge=1)

class UpdateAccountBalanceResponse(BaseModel):
    id: str
    balance: float

class Account(BaseModel):
    id: str
    account_number: str
    holder_name: str
    account_type: str
    balance: float
    currency: str

class Accounts(BaseModel):
    accounts: list[Account]