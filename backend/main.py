from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Inicializa a aplicação FastAPI
app = FastAPI(title="Gerenciador Financeiro")

# Configuração de CORS (Cross-Origin Resource Sharing)
# Permite que o Front-End (HTML/JS) acesse este Back-End sem ser bloqueado pelo navegador por segurança.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Libera acesso para qualquer origem durante o desenvolvimento
    allow_credentials=True,
    allow_methods=["*"], # Libera métodos HTTP (GET, POST, PUT, DELETE)
    allow_headers=["*"],
)

# Rota principal (endpoint) para testar o funcionamento da API
@app.get("/")
def home():
    return {"status": "Sucesso", "mensagem": "API Financeira rodando!"}