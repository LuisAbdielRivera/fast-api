from fastapi import HTTPException, Request, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from jwt_config import valida_token
import src.crud.usuario, src.config.db, src.models.usuario

src.models.usuario.base.metadata.create_all(bind=src.config.db.engine)


def get_db():
    db = src.config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Portador(HTTPBearer):
    async def call(self, request: Request, db: Session = Depends(get_db)):
        autorizacion = await super().call(request)
        dato = valida_token(autorizacion.credentials)
        db_userlogin = src.crud.usuario.get_user_by_credentials(db,
            username=dato["user_name"],
            correo=dato["email"],
            telefono=dato["phone_number"],
            password=dato["password"])
        if db_userlogin is None:
            raise HTTPException(status_code=404, detail="Login incorrecto")
        return db_userlogin