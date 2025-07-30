from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from models.consulta import Consulta
from models.medico import Medico
from models.clinica import Clinica
from models.paciente import Paciente
from datetime import datetime, date

# -------------------- CRUD CONSULTA --------------------

def create_consulta(db: Session, id_paciente: int, id_medico: int, id_clinica: int, data_consulta, observacoes=None):
    """
    Agenda uma consulta usando a procedure SQL 'agendar_consulta'.
    Retorna True se sucesso, False se erro.
    """
    try:
        db.execute(text(
            "CALL agendar_consulta(:p_paciente_id, :p_medico_id, :p_clinica_id, :p_data, :p_obs)"
        ), {
            "p_paciente_id": id_paciente,
            "p_medico_id": id_medico,
            "p_clinica_id": id_clinica,
            "p_data": data_consulta,
            "p_obs": observacoes
        })
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Erro ao agendar consulta: {e}")
        return False

def get_consultas_futuras(db: Session, data_minima: date = None):
    """
    Retorna uma lista de consultas futuras da view vw_consultas_futuras.
    Se data_minima for fornecida, filtra consultas com data_consulta >= data_minima.
    """
    try:
        if data_minima:
            # Filtra com data_consulta >= data_minima usando SQL raw query
            query = text("SELECT * FROM vw_consultas_futuras WHERE data_consulta >= :data_minima ORDER BY data_consulta")
            result = db.execute(query, {"data_minima": data_minima})
        else:
            query = text("SELECT * FROM vw_consultas_futuras ORDER BY data_consulta")
            result = db.execute(query)
        return result.fetchall()
    except SQLAlchemyError as e:
        print(f"Erro ao buscar consultas futuras: {e}")
        return []

def get_consulta_by_id(db: Session, consulta_id: int):
    """
    Busca uma consulta pelo ID.
    """
    return db.query(Consulta).filter(Consulta.id == consulta_id).first()

def get_all_consultas(db: Session):
    """
    Retorna todas as consultas cadastradas.
    """
    return db.query(Consulta).all()

def update_consulta(db: Session, consulta_id: int, **kwargs):
    """
    Atualiza campos de uma consulta pelo ID.
    """
    consulta = get_consulta_by_id(db, consulta_id)
    if not consulta:
        return None
    try:
        for key, value in kwargs.items():
            setattr(consulta, key, value)
        db.commit()
        db.refresh(consulta)
        return consulta
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Erro ao atualizar consulta: {e}")
        return None

def delete_consulta(db: Session, consulta_id: int):
    """
    Deleta uma consulta pelo ID.
    """
    consulta = get_consulta_by_id(db, consulta_id)
    if not consulta:
        return False
    try:
        db.delete(consulta)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Erro ao deletar consulta: {e}")
        return False

def get_consultas_by_paciente_id(db: Session, paciente_id: int):
    """
    Retorna todas as consultas associadas a um paciente pelo ID do paciente.
    """
    try:
        return db.query(Consulta).filter(Consulta.id_paciente == paciente_id).all()
    except SQLAlchemyError as e:
        print(f"Erro ao buscar consultas do paciente {paciente_id}: {e}")
        return []

# -------------------- BUSCAS COMPLEMENTARES --------------------

def buscar_medicos_por_nome(db: Session, nome: str):
    """
    Busca médicos cujo nome contenha a string fornecida.
    """
    try:
        return db.query(Medico).filter(Medico.nome.ilike(f"%{nome}%")).all()
    except SQLAlchemyError as e:
        print(f"Erro ao buscar médicos: {e}")
        return []

def buscar_pacientes_por_nome(db: Session, nome: str):
    """
    Busca pacientes cujo nome contenha a string fornecida.
    """
    try:
        return db.query(Paciente).filter(Paciente.nome.ilike(f"%{nome}%")).all()
    except SQLAlchemyError as e:
        print(f"Erro ao buscar pacientes: {e}")
        return []

def get_todas_clinicas(db: Session):
    """
    Retorna todas as clínicas disponíveis.
    """
    try:
        return db.query(Clinica).all()
    except SQLAlchemyError as e:
        print(f"Erro ao buscar clínicas: {e}")
        return []
