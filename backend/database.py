from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Definimos a URL do banco de dados (SQLite salvará tudo em um arquivo local 'finance.db')
SQLALCHEMY_DATABASE_URL = "sqlite:///./finance.sqlite3"

# 2. Criamos o "Engine", que é o motor de conexão do SQLAlchemy com o banco de dados.
# O parâmetro 'check_same_thread: False' é necessário apenas para o SQLite no FastAPI.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Criamos a fabrica de sessões (SessionLocal). Cada requisição à API abrirá uma sessão para ler/escrever dados.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Classe base da qual nossos modelos de tabelas herdarão.
Base = declarative_base()

# 5. Função utilitária (Dependency Injection) para gerenciar o ciclo de vida do banco em cada requisição.
def get_db():
    db = SessionLocal()
    try:
        yield db  # Entrega a sessão do banco para a rota usar
    finally:
        db.close()  # Garante que a conexão seja FECHADA após o fim da requisição