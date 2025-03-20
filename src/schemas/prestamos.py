from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class PrestamoBase(BaseModel):
    id_usuario: int
    id_material: int
    fecha_prestamo: datetime
    fecha_devolucion: Optional[datetime] = None
    estado_prestamo: str

class PrestamoCreate(PrestamoBase):
    pass

class PrestamoUpdate(PrestamoBase):
    pass

class Prestamo(PrestamoBase):
    id_prestamo: int
    class Config:
        orm_mode = True
