from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from src.config.db import base
import enum

class EstadoPrestamo(str, enum.Enum):
    Activo = "Activo"
    Devuelto = "Devuelto"
    Vencido = "Vencido"

class Prestamo(base):
    __tablename__ = "tbb_prestamos"

    id_prestamo = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("tbb_usuarios.id"), nullable=False)
    id_material = Column(Integer, ForeignKey("tbb_materiales.id_material"), nullable=False)
    fecha_prestamo = Column(DateTime, nullable=False)
    fecha_devolucion = Column(DateTime, nullable=True)
    estado_prestamo = Column(Enum(EstadoPrestamo), nullable=False)

    usuario = relationship("User", backref="prestamos")
    material = relationship("Material", backref="prestamos")
