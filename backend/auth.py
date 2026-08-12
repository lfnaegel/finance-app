from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from backend.database import get_db
import backend.models as models

# Configurações de Segurança do JWT (Gratuito e Local)
SECRET_KEY = "sua_chave_secreta_super_segura_para_desenvolvimento_finance_app"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # O token expira em 24 horas

# Define o algoritmo de hash para senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Indica para o FastAPI qual rota é responsável por emitir o token de login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# 1. Criptografar Senha
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# 2. Verificar se a senha digitada corresponde ao hash do banco
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# 3. Gerar o Token JWT
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 4. Middleware/Função para proteger rotas (Pega o usuário atual através do Token)
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível me autenticar ou token expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user