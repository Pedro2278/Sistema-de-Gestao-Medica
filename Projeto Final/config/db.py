# config/db.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Ajuste aqui os dados conforme seu MySQL
USER = 'root'
PASSWORD = 'pedro'
HOST = '127.0.0.1'
PORT = '3306'
DB_NAME = 'projeto_final'

# URL de conexão
DATABASE_URL = f'mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}'

# Criar engine
engine = create_engine(DATABASE_URL, echo=True)

# Criar sessão
SessionLocal = sessionmaker(bind=engine)

# Base para os modelos
Base = declarative_base()
