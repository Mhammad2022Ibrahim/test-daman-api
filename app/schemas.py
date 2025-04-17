from pydantic import BaseModel, Field, EmailStr, validator, field_serializer, ConfigDict
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime

class CreateAccount(BaseModel):
    name: str
    email: EmailStr
    balance: float = Field(default=0.0, ge=0.0)
    phone: Optional[str] = None
    address: Optional[str] = None

class AccountResponse(BaseModel):
    id: int
    name: str
    balance:float
    message: str

    model_config = ConfigDict(from_attributes=True)


class ErrorResponse(BaseModel):
    message: str

class UpdateAccount(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    balance: Optional[float] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class TransactionType(str, Enum):
    deposit = "deposit"
    withdrawal = "withdrawal"

class CreateTransaction(BaseModel):
    account_id: int
    amount: float
    transaction_type: TransactionType

class TransactionResponse(BaseModel):
    account_id: int
    amount: float
    transaction_type: TransactionType
    balance: float

class ShowTransaction(BaseModel):
    id: int
    amount: float
    account_id: int
    created_at: datetime
    updated_at: datetime

    @field_serializer("created_at", "updated_at")
    def serialize_date(self, dt: datetime, _info):
        return dt.strftime("%Y-%m-%d") 

    model_config = ConfigDict(from_attributes=True)