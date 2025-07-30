from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.paciente import Paciente
from models.consulta import Consulta

def create_paciente(db: Session, nome: str, cpf: str, telefone: str = None, email: str = None):
    paciente = Paciente(nome=nome, cpf=cpf, telefone=telefone, email=email)
    db.add(paciente)
    db.commit()
    db.refresh(paciente)
    return paciente

def get_paciente_by_id(db: Session, paciente_id: int):
    return db.query(Paciente).filter(Paciente.id == paciente_id).first()

def get_all_pacientes(db: Session):
    return db.query(Paciente).all()

def buscar_pacientes_por_nome(db: Session, nome: str):
    return db.query(Paciente).filter(Paciente.nome.ilike(f"%{nome}%")).all()

def update_paciente(db: Session, paciente_id: int, **kwargs):
    paciente = get_paciente_by_id(db, paciente_id)
    if not paciente:
        return None
    for key, value in kwargs.items():
        if hasattr(paciente, key) and value is not None:
            setattr(paciente, key, value)
    db.commit()
    db.refresh(paciente)
    return paciente

def delete_paciente(db: Session, paciente_id: int):
    paciente = get_paciente_by_id(db, paciente_id)
    if not paciente:
        return False
    try:
        # Deleta consultas relacionadas (evita erro de integridade referencial)
        consultas_relacionadas = db.query(Consulta).filter(Consulta.paciente_id == paciente_id).all()
        for consulta in consultas_relacionadas:
            db.delete(consulta)

        # Agora deleta o paciente
        db.delete(paciente)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        print(f"[ERRO] Falha ao deletar paciente e suas consultas: {e}")
        return False
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.paciente import Paciente
from models.consulta import Consulta

def create_paciente(db: Session, nome: str, cpf: str, telefone: str = None, email: str = None):
    paciente = Paciente(nome=nome, cpf=cpf, telefone=telefone, email=email)
    db.add(paciente)
    db.commit()
    db.refresh(paciente)
    return paciente

def get_paciente_by_id(db: Session, paciente_id: int):
    return db.query(Paciente).filter(Paciente.id == paciente_id).first()

def get_all_pacientes(db: Session):
    return db.query(Paciente).all()

def buscar_pacientes_por_nome(db: Session, nome: str):
    return db.query(Paciente).filter(Paciente.nome.ilike(f"%{nome}%")).all()

def update_paciente(db: Session, paciente_id: int, **kwargs):
    paciente = get_paciente_by_id(db, paciente_id)
    if not paciente:
        return None
    for key, value in kwargs.items():
        if hasattr(paciente, key) and value is not None:
            setattr(paciente, key, value)
    db.commit()
    db.refresh(paciente)
    return paciente

def delete_paciente(db: Session, paciente_id: int):
    paciente = get_paciente_by_id(db, paciente_id)
    if not paciente:
        return False
    try:
        # Deleta consultas relacionadas (evita erro de integridade referencial)
        consultas_relacionadas = db.query(Consulta).filter(Consulta.id_paciente == paciente_id).all()
        for consulta in consultas_relacionadas:
            db.delete(consulta)

        # Agora deleta o paciente
        db.delete(paciente)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        print(f"[ERRO] Falha ao deletar paciente e suas consultas: {e}")
        return False
