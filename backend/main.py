from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import engine, Base
import backend.models as model

#cria as tabelas no banco de dados SQLite caso elas ainda não existam
Base.metadata.create_all(bind=engine)

# inicializa a aplicação FastAPI
app = FastAPI(title="Gerenciador Financeiro")

# Configuração de CORS (Cross-Origin Resource Sharing)
# Permite que o Front-End (HTML/JS) acesse este Back-End sem ser bloqueado pelo navegador por segurança.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rota principal (endpoint) para testar o funcionamento da API
@app.get("/")
def home():
    return {"status": "Sucesso", "mensagem": "API Financeira rodando!"}