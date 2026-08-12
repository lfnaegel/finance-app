from pydantic import BaseModel
from typing import Literal

# Estrutura base com os campos comuns
class TransactionBase(BaseModel):
    description: str
    value: float
    type: Literal["receita", "despesa"]  
    date: str  

# Schema usado na requisição de CRIAÇÃO (recebe os dados do front-end)
class TransactionCreate(TransactionBase):
    pass

# Schema usado na RESPOSTA da API (devolve os dados já salvos + o ID do banco)
class TransactionResponse(TransactionBase):
    id: int

    class Config:
        from_attributes = True  # Permite ler direto do objeto SQLAlchemy