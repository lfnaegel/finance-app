from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from backend.database import engine, Base, get_db
import backend.models as models
import backend.schemas as schemas
import backend.auth as auth

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# Atualiza/Cria as tabelas no SQLite
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gerenciador Financeiro")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- AUTENTICAÇÃO ---

@app.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    # Verifica se e-mail já existe
    db_user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    
    # Criptografa a senha antes de salvar
    hashed_pwd = auth.hash_password(user_data.password)
    new_user = models.User(email=user_data.email, hashed_password=hashed_pwd)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # O form_data usa o campo 'username' para receber o e-mail
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="E-mail ou senha incorretos")
    
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# --- TRANSAÇÕES PROTEGIDAS (Exigem Login) ---

@app.post("/transactions", response_model=schemas.TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(
    transaction: schemas.TransactionCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # Vincula automaticamente a transação ao ID do usuário logado
    db_transaction = models.Transaction(**transaction.model_dump(), user_id=current_user.id)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@app.get("/transactions", response_model=List[schemas.TransactionResponse])
def read_transactions(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # Retorna apenas as transações pertencentes ao usuário logado
    return db.query(models.Transaction).filter(models.Transaction.user_id == current_user.id).all()

@app.get("/transactions/summary", response_model=schemas.SummaryResponse)
def get_summary(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    transactions = db.query(models.Transaction).filter(models.Transaction.user_id == current_user.id).all()
    total_income = sum(t.value for t in transactions if t.type == "receita")
    total_expense = sum(t.value for t in transactions if t.type == "despesa")
    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": total_income - total_expense
    }

@app.delete("/transactions/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(
    transaction_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_transaction = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id,
        models.Transaction.user_id == current_user.id
    ).first()
    
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    
    db.delete(db_transaction)
    db.commit()
    return None

# Servir arquivos estáticos do front-end
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")

app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/", response_class=FileResponse)
def read_index():
    return os.path.join(frontend_path, "index.html")