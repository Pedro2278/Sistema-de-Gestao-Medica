from sqlalchemy import Column, Integer, String, Date
from config.db import Base
from sqlalchemy.orm import relationship

class Paciente(Base):
    __tablename__ = 'paciente'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False)
    data_nascimento = Column(Date)
    telefone = Column(String(20))
    email = Column(String(100))

    consultas = relationship("Consulta", back_populates="paciente", cascade="all, delete")

