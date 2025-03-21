"""Módulo principal para la API de PRESTAMOS S.A. de C.V."""

from fastapi import FastAPI
from src.routes.usuarios import usuarios
from src.routes.material import material
from src.routes.prestamos import prestamo
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="PRESTAMOS S.A. de C.V.",
    description="API para el almacenamiento de información de préstamo de equipo informático",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes cambiar "*" por ["http://localhost:5500"] si solo quieres permitir ese origen
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de PRESTAMOS S.A. de C.V."}

app.include_router(usuarios)
app.include_router(material)
app.include_router(prestamo)
