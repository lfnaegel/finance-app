from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from backend.database import engine, Base, get_db
import backend.models as models
import backend.schemas as schemas

# Cria a tabela no arquivo SQLite caso não exista
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gerenciador Financeiro")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. ROTA DE CRIAÇÃO (CREATE)
@app.post("/transactions", response_model=schemas.TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    # Converte os dados do Pydantic para o modelo da tabela
    db_transaction = models.Transaction(**transaction.model_dump())
    db.add(db_transaction)       # Adiciona à fila de inserção
    db.commit()                  # Executa o comando de gravação no banco
    db.refresh(db_transaction)   # Recarrega para pegar o ID gerado automaticamente
    return db_transaction

# 2. ROTA DE LISTAGEM (READ)
@app.get("/transactions", response_model=List[schemas.TransactionResponse])
def read_transactions(db: Session = Depends(get_db)):
    # Consulta todos os registros armazenados na tabela
    transactions = db.query(models.Transaction).all()
    return transactions