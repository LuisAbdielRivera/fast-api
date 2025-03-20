"""Módulo CRUD para la gestión de materiales en la base de datos."""

from sqlalchemy.orm import Session
from src.models.material import Material
from src.schemas.material import MaterialCreate, MaterialUpdate

def get_material(db: Session, material_id: int):
    """Obtiene un material por su ID."""
    return db.query(Material).filter(Material.id_material == material_id).first()

def get_material_by_tipo(db: Session, tipo_material: str):
    """Obtiene un material por su tipo."""
    return db.query(Material).filter(Material.tipo_material == tipo_material).first()

def create_material(db: Session, material: MaterialCreate):
    """Crea un nuevo material en la base de datos."""
    db_material = Material(
        tipo_material=material.tipo_material,
        marca=material.marca,
        modelo=material.modelo,
        estado=material.estado
    )
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material

def update_material(db: Session, material_id: int, material: MaterialUpdate):
    """Actualiza los datos de un material existente."""
    db_material = db.query(Material).filter(Material.id_material == material_id).first()
    if db_material:
        for var, value in vars(material).items():
            if value is not None:
                setattr(db_material, var, value)
        db.commit()
        db.refresh(db_material)
    return db_material

def delete_material(db: Session, material_id: int):
    """Elimina un material de la base de datos."""
    db_material = db.query(Material).filter(Material.id_material == material_id).first()
    if db_material:
        db.delete(db_material)
        db.commit()
    return db_material

def get_materials(db: Session, skip: int = 0, limit: int = 10):
    """Obtiene una lista paginada de materiales."""
    return db.query(Material).offset(skip).limit(limit).all()
