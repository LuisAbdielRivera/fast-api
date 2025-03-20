"""
Módulo CRUD para la gestión de usuarios en la base de datos.
"""

from sqlalchemy.orm import Session
from src.models.usuario import User
from src.schemas.usuario import UserCreate, UserUpdate


def get_user(db: Session, user_id: int):
    """
    Obtiene un usuario por su ID.
    """
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    """
    Obtiene un usuario por su nombre de usuario.
    """
    return db.query(User).filter(User.nombreUsuario == username).first()


def create_user(db: Session, user: UserCreate):
    """
    Crea un nuevo usuario en la base de datos.
    """
    db_user = User(
        nombre=user.nombre,
        primerApellido=user.primerApellido,
        segundoApellido=user.segundoApellido,
        tipoUsuario=user.tipoUsuario,
        nombreUsuario=user.nombreUsuario,
        correoElectronico=user.correoElectronico,
        contrasena=user.contrasena,
        numeroTelefonico=user.numeroTelefonico,
        estatus=user.estatus,
        fechaRegistro=user.fechaRegistro,
        fechaActualizacion=user.fechaActualizacion,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user: UserUpdate):
    """
    Actualiza la información de un usuario por su ID.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        for var, value in vars(user).items():
            if value is not None:
                setattr(db_user, var, value)
        db.commit()
        db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    """
    Elimina un usuario de la base de datos por su ID.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user


def get_user_by_credentials(db: Session, username: str, correo: str, telefono: str, password: str):
    """
    Obtiene un usuario que coincida con sus credenciales (usuario, correo o teléfono y contraseña).
    """
    return (
        db.query(User)
        .filter(
            (User.nombreUsuario == username) |
            (User.correoElectronico == correo) |
            (User.numeroTelefonico == telefono),
            User.contrasena == password
        )
        .first()
    )


def get_users(db: Session, skip: int = 0, limit: int = 10):
    """
    Obtiene una lista de usuarios paginada.
    """
    return db.query(User).offset(skip).limit(limit).all()
