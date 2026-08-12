from pydantic import BaseModel, EmailStr
from typing import Literal, Optional

# Schemas de Usuários
class UserCreate(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True

# Schemas de Token JWT
class Token(BaseModel):
    access_token: str
    token_type: str

# Schemas de Transação
class TransactionBase(BaseModel):
    description: str
    value: float
    type: Literal["receita", "despesa"]
    category: str
    date: str

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    description: Optional[str] = None
    value: Optional[float] = None
    type: Optional[Literal["receita", "despesa"]] = None
    category: Optional[str] = None
    date: Optional[str] = None

class TransactionResponse(TransactionBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class SummaryResponse(BaseModel):
    total_income: float
    total_expense: float
    balance: float