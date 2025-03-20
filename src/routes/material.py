from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import src.crud.material
import src.config.db
import src.schemas.material
import src.models.material
from typing import List
from portadortoken import Portador

material = APIRouter()

src.models.material.base.metadata.create_all(bind=src.config.db.engine)

def get_db():
    db = src.config.db.SesionLocal()
    try:
        yield db
    finally:
        db.close()

@material.get(
    "/materials/", 
    response_model=List[src.schemas.material.Material], 
    tags=["Materiales"],
    dependencies=[Depends(Portador())]
)
async def read_materials(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_materials = src.crud.material.get_materials(db=db, skip=skip, limit=limit)
    return db_materials

@material.get(
    "/material/{id}", 
    response_model=src.schemas.material.Material, 
    tags=["Materiales"],
    dependencies=[Depends(Portador())]
)
async def read_material(id: int, db: Session = Depends(get_db)):
    db_material = src.crud.material.get_material(db=db, material_id=id)
    if db_material is None:
        raise HTTPException(status_code=404, detail="Material no encontrado")
    return db_material

@material.post(
    "/material/", 
    response_model=src.schemas.material.Material, 
    tags=["Materiales"],
    dependencies=[Depends(Portador())]
)
def create_material(material: src.schemas.material.MaterialCreate, db: Session = Depends(get_db)):
    return src.crud.material.create_material(db=db, material=material)

@material.put(
    "/material/{id}", 
    response_model=src.schemas.material.Material, 
    tags=["Materiales"],
    dependencies=[Depends(Portador())]
)
async def update_material(id: int, material: src.schemas.material.MaterialUpdate, db: Session = Depends(get_db)):
    db_material = src.crud.material.update_material(db=db, material_id=id, material=material)
    if db_material is None:
        raise HTTPException(status_code=404, detail="Material no existe, no actualizado")
    return db_material

@material.delete(
    "/material/{id}", 
    response_model=src.schemas.material.Material, 
    tags=["Materiales"],
    dependencies=[Depends(Portador())]
)
async def delete_material(id: int, db: Session = Depends(get_db)):
    db_material = src.crud.material.delete_material(db=db, material_id=id)
    if db_material is None:
        raise HTTPException(status_code=404, detail="Material no existe, no se pudo eliminar")
    return db_material
