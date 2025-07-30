from sqlalchemy import Column, Integer, String
from config.db import Base

class Clinica(Base):
    __tablename__ = "clinica"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    endereco = Column(String(200), nullable=True)

    def __repr__(self):
        return f"<Clinica(id={self.id}, nome='{self.nome}')>"
