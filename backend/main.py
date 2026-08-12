from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from backend.database import engine, Base, get_db
import backend.models as models
import backend.schemas as schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gerenciador Financeiro")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. CRIAR
@app.post("/transactions", response_model=schemas.TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    db_transaction = models.Transaction(**transaction.model_dump())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

# 2. LISTAR TODAS
@app.get("/transactions", response_model=List[schemas.TransactionResponse])
def read_transactions(db: Session = Depends(get_db)):
    return db.query(models.Transaction).all()

# 3. RESUMO FINANCEIRO (Saldo, Receitas, Despesas)
@app.get("/transactions/summary", response_model=schemas.SummaryResponse)
def get_summary(db: Session = Depends(get_db)):
    transactions = db.query(models.Transaction).all()
    total_income = sum(t.value for t in transactions if t.type == "receita")
    total_expense = sum(t.value for t in transactions if t.type == "despesa")
    balance = total_income - total_expense
    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance
    }

# 4. ATUALIZAR (PUT)
@app.put("/transactions/{transaction_id}", response_model=schemas.TransactionResponse)
def update_transaction(transaction_id: int, updated_data: schemas.TransactionUpdate, db: Session = Depends(get_db)):
    db_transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    
    # Atualiza apenas os campos enviados pelo usuário
    update_dict = updated_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(db_transaction, key, value)
    
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

# 5. DELETAR (DELETE)
@app.delete("/transactions/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    
    db.delete(db_transaction)
    db.commit()
    return None