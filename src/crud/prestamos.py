"""Módulo CRUD para la gestión de préstamos en la base de datos."""

from sqlalchemy.orm import Session
from src.models.prestamos import Prestamo
from src.schemas.prestamos import PrestamoCreate, PrestamoUpdate

def get_prestamo(db: Session, prestamo_id: int):
    """Obtiene un préstamo por su ID."""
    return db.query(Prestamo).filter(Prestamo.id_prestamo == prestamo_id).first()

def get_prestamos(db: Session, skip: int = 0, limit: int = 10):
    """Obtiene una lista paginada de préstamos."""
    return db.query(Prestamo).offset(skip).limit(limit).all()

def create_prestamo(db: Session, prestamo: PrestamoCreate):
    """Crea un nuevo préstamo en la base de datos."""
    db_prestamo = Prestamo(
        id_usuario=prestamo.id_usuario,
        id_material=prestamo.id_material,
        fecha_prestamo=prestamo.fecha_prestamo,
        fecha_devolucion=prestamo.fecha_devolucion,
        estado_prestamo=prestamo.estado_prestamo
    )
    db.add(db_prestamo)
    db.commit()
    db.refresh(db_prestamo)
    return db_prestamo

def update_prestamo(db: Session, prestamo_id: int, prestamo: PrestamoUpdate):
    """Actualiza un préstamo existente."""
    db_prestamo = db.query(Prestamo).filter(Prestamo.id_prestamo == prestamo_id).first()
    if db_prestamo:
        for var, value in vars(prestamo).items():
            if value is not None:
                setattr(db_prestamo, var, value)
        db.commit()
        db.refresh(db_prestamo)
    return db_prestamo

def delete_prestamo(db: Session, prestamo_id: int):
    """Elimina un préstamo de la base de datos."""
    db_prestamo = db.query(Prestamo).filter(Prestamo.id_prestamo == prestamo_id).first()
    if db_prestamo:
        db.delete(db_prestamo)
        db.commit()
    return db_prestamo
