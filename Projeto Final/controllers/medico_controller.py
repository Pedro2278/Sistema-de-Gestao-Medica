from sqlalchemy.orm import Session, joinedload
from models.medico import Medico
from models.especialidade import Especialidade

def create_medico(db: Session, nome: str, crm: str, id_especialidade: int = None):
    medico = Medico(nome=nome, crm=crm, especialidade_id=id_especialidade)
    db.add(medico)
    db.commit()
    db.refresh(medico)
    return medico

def get_medico_by_id(db: Session, medico_id: int):
    return db.query(Medico).filter(Medico.id == medico_id).first()

def get_all_medicos(db: Session):
    return db.query(Medico).all()

def listar_medicos_com_especialidades(db: Session):
    return db.query(Medico).options(joinedload(Medico.especialidade)).all()

def update_medico(db: Session, medico_id: int, **kwargs):
    medico = get_medico_by_id(db, medico_id)
    if not medico:
        return None
    for key, value in kwargs.items():
        setattr(medico, key, value)
    db.commit()
    db.refresh(medico)
    return medico

def delete_medico(db: Session, medico_id: int):
    medico = get_medico_by_id(db, medico_id)
    if not medico:
        return False
    db.delete(medico)
    db.commit()
    return True
