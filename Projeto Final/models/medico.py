from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base

class Medico(Base):
    __tablename__ = "medico"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    crm = Column(String(20), nullable=False, unique=True)
    especialidade_id = Column(Integer, ForeignKey("especialidade.id"))

    especialidade = relationship("Especialidade", backref="medicos")
