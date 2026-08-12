from sqlalchemy import Column, Integer, String, Float
from backend.database import Base

class Transaction(Base):
    # Nome da tabela que será criada no banco de dados SQLite
    __tablename__ = "transactions"

    # Colunas da tabela
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    description = Column(String, nullable=False)   
    value = Column(Float, nullable=False)          
    type = Column(String, nullable=False)          
    category = Column(String, nullable=False)      
    date = Column(String, nullable=False)          