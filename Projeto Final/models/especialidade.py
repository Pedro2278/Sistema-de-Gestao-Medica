from sqlalchemy import Column, Integer, String
from config.db import Base

class Especialidade(Base):
    __tablename__ = "especialidade"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
