from sqlalchemy import Column, Integer, ForeignKey, Date
from config.db import Base
from sqlalchemy.orm import relationship

class Consulta(Base):
    __tablename__ = 'consultas'

    id = Column(Integer, primary_key=True, index=True)
    id_paciente = Column(Integer, ForeignKey('paciente.id'))
    id_medico = Column(Integer, ForeignKey('medicos.id'), nullable=False)
    data_consulta = Column(Date, nullable=False)

    paciente = relationship("Paciente", back_populates="consultas")
