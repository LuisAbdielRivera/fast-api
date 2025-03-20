from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import src.crud.prestamos
import src.config.db
import src.schemas.prestamos
import src.models.prestamos
from typing import List
from portadortoken import Portador

prestamo = APIRouter()

src.models.prestamos.base.metadata.create_all(bind=src.config.db.engine)

def get_db():
    db = src.config.db.SesionLocal()
    try:
        yield db
    finally:
        db.close()

@prestamo.get(
    "/prestamos/", 
    response_model=List[src.schemas.prestamos.Prestamo], 
    tags=["Préstamos"],
    dependencies=[Depends(Portador())]
)
async def read_prestamos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return src.crud.prestamos.get_prestamos(db=db, skip=skip, limit=limit)

@prestamo.get(
    "/prestamo/{id}", 
    response_model=src.schemas.prestamos.Prestamo, 
    tags=["Préstamos"],
    dependencies=[Depends(Portador())]
)
async def read_prestamo(id: int, db: Session = Depends(get_db)):
    db_prestamo = src.crud.prestamos.get_prestamo(db=db, prestamo_id=id)
    if db_prestamo is None:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    return db_prestamo

@prestamo.post(
    "/prestamos/", 
    response_model=src.schemas.prestamos.Prestamo, 
    tags=["Préstamos"],
    dependencies=[Depends(Portador())]
)
def create_prestamo(prestamo: src.schemas.prestamos.PrestamoCreate, db: Session = Depends(get_db)):
    return src.crud.prestamos.create_prestamo(db=db, prestamo=prestamo)

@prestamo.put(
    "/prestamo/{id}", 
    response_model=src.schemas.prestamos.Prestamo, 
    tags=["Préstamos"],
    dependencies=[Depends(Portador())]
)
async def update_prestamo(id: int, prestamo: src.schemas.prestamos.PrestamoUpdate, db: Session = Depends(get_db)):
    db_prestamo = src.crud.prestamos.update_prestamo(db=db, prestamo_id=id, prestamo=prestamo)
    if db_prestamo is None:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado, no actualizado")
    return db_prestamo

@prestamo.delete(
    "/prestamo/{id}", 
    response_model=src.schemas.prestamos.Prestamo, 
    tags=["Préstamos"],
    dependencies=[Depends(Portador())]
)
async def delete_prestamo(id: int, db: Session = Depends(get_db)):
    db_prestamo = src.crud.prestamos.delete_prestamo(db=db, prestamo_id=id)
    if db_prestamo is None:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado, no eliminado")
    return db_prestamo
