"""
Backend del recomendador: FastAPI + CLIPS (clipspy)

Instalar:  pip install fastapi uvicorn clipspy
Ejecutar desde la raíz del proyecto:  python -m uvicorn backend.main:app --reload
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .modelos import OpcionesDisponibles, ResultadoRecomendacion, SolicitudRecomendacion
from .motor_experto import evaluar_recomendacion, obtener_opciones

app = FastAPI(title="Recomendador del comedor")

# Ajusta los orígenes a donde sirvas tu frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/opciones", response_model=OpcionesDisponibles)
def opciones():
    return obtener_opciones()


@app.post("/api/recomendar", response_model=ResultadoRecomendacion)
def recomendar(solicitud: SolicitudRecomendacion):
    try:
        return evaluar_recomendacion(solicitud.categoria, solicitud.ingrediente)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
