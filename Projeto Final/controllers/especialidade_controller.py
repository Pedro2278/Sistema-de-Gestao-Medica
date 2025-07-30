from sqlalchemy.orm import Session
from models.especialidade import Especialidade

def create_especialidade(db: Session, nome: str):
    especialidade = Especialidade(nome=nome)
    db.add(especialidade)
    db.commit()
    db.refresh(especialidade)
    return especialidade

def get_especialidade_by_id(db: Session, especialidade_id: int):
    return db.query(Especialidade).filter(Especialidade.id == especialidade_id).first()

def get_all_especialidades(db: Session):
    return db.query(Especialidade).all()

def update_especialidade(db: Session, especialidade_id: int, **kwargs):
    especialidade = get_especialidade_by_id(db, especialidade_id)
    if not especialidade:
        return None
    for key, value in kwargs.items():
        setattr(especialidade, key, value)
    db.commit()
    db.refresh(especialidade)
    return especialidade

def delete_especialidade(db: Session, especialidade_id: int):
    especialidade = get_especialidade_by_id(db, especialidade_id)
    if not especialidade:
        return False
    db.delete(especialidade)
    db.commit()
    return True
