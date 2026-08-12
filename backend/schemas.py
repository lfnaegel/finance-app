from pydantic import BaseModel
from typing import Literal, Optional

# Base comum
class TransactionBase(BaseModel):
    description: str
    value: float
    type: Literal["receita", "despesa"]
    category: str
    date: str

class TransactionCreate(TransactionBase):
    pass

# Schema de Atualização: todos os campos tornam-se opcionais (= None)
class TransactionUpdate(BaseModel):
    description: Optional[str] = None
    value: Optional[float] = None
    type: Optional[Literal["receita", "despesa"]] = None
    category: Optional[str] = None
    date: Optional[str] = None

class TransactionResponse(TransactionBase):
    id: int

    class Config:
        from_attributes = True

# Schema do Resumo Financeiro
class SummaryResponse(BaseModel):
    total_income: float
    total_expense: float
    balance: float