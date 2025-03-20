from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import src.crud.usuario
import src.config.db
import src.schemas.usuario
import src.models.usuario
from typing import List
from portadortoken import Portador
from fastapi.responses import JSONResponse
from jwt_config import solicita_token

usuarios = APIRouter()

src.models.usuario.base.metadata.create_all(bind=src.config.db.engine)


def get_db():
    db = src.config.db.SesionLocal()
    try:
        yield db
    finally:
        db.close()


@usuarios.get(
    "/users/", 
    response_model=List[src.schemas.usuario.User], 
    tags=["Usuarios"], 
    dependencies=[Depends(Portador())]
)
async def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_users = src.crud.usuario.get_users(db=db, skip=skip, limit=limit)
    return db_users


@usuarios.get(
    "/user/{id}", 
    response_model=src.schemas.usuario.User, 
    tags=["Usuarios"],
    dependencies=[Depends(Portador())]
)
async def read_user(id: int, db: Session = Depends(get_db)):
    db_user = src.crud.usuario.get_user(db=db, user_id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@usuarios.post(
    "/users/", 
    response_model=src.schemas.usuario.User, 
    tags=["Usuarios"]
)
def create_user(user: src.schemas.usuario.UserCreate, db: Session = Depends(get_db)):
    db_user = src.crud.usuario.get_user_by_username(db, username=user.nombreUsuario)
    if db_user:
        raise HTTPException(
            status_code=400, detail="Usuario existente intenta nuevamente"
        )
    return src.crud.usuario.create_user(db=db, user=user)


@usuarios.put(
    "/user/{id}", 
    response_model=src.schemas.usuario.User, 
    tags=["Usuarios"], 
    dependencies=[Depends(Portador())]
)
async def update_user(
    id: int, user: src.schemas.usuario.UserUpdate, db: Session = Depends(get_db)
):
    db_user = src.crud.usuario.update_user(db=db, user_id=id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no existe, no actualizado")
    return db_user


@usuarios.delete(
    "/user/{id}", 
    response_model=src.schemas.usuario.User, 
    tags=["Usuarios"],
    dependencies=[Depends(Portador())]
)
async def delete_user(id: int, db: Session = Depends(get_db)):
    db_user = src.crud.usuario.delete_user(db=db, user_id=id)
    if db_user is None:
        raise HTTPException(
            status_code=404, detail="Usuario no existe, no se pudo eliminar"
        )
    return db_user

@usuarios.post("/login", tags=["User Login"])
def read_credentials(ususario: src.schemas.usuario.UserLogin, db: Session = Depends(get_db)):
    db_credentials = src.crud.usuario.get_user_by_credentials(
        db,
        username=ususario.nombreUsuario,
        password=ususario.contrasena,
        correo=ususario.correoElectronico,
        telefono=ususario.numeroTelefonico
    )
    if db_credentials is None:
        return JSONResponse(content={'mensaje': 'Acceso denegado'}, status_code=404)

    # Se genera el token y se retorna en la respuesta
    token: str = solicita_token(ususario.dict())
    return JSONResponse(status_code=200, content={"token": token})
