from sqlalchemy import Column, Integer, String, Enum
from src.config.db import base
import enum

class EstadoMaterial(str, enum.Enum):
    Disponible = "Disponible"
    Prestado = "Prestado"
    En_Mantenimiento = "En Mantenimiento"
    Dañado = "Dañado"
    No_Disponible = "No Disponible"

class Material(base):
    __tablename__ = "tbb_materiales"

    id_material = Column(Integer, primary_key=True, autoincrement=True)
    tipo_material = Column(String(50), nullable=False)
    marca = Column(String(50), nullable=False)
    modelo = Column(String(50), nullable=False)
    estado = Column(Enum(EstadoMaterial), nullable=False)