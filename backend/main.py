from fastapi import FastAPI
from .modelos import SolicitudRefaccion, ResultadoRefaccion
from .motor_experto import evaluar_refaccion


app = FastAPI(
    title="Sistema Experto de Refacciones",
    description="API REST para exponer el motor experto de refacciones mediante python",
    version="1.0.0",
)

@app.get("/api/v1/health")
def health():
    return {
        "estado": "OK",
        "sistema": "Refacciones",
        "motor": "CLIPS",
        "integracion": "clipspy",
    }

@app.post("/api/v1/evaluar", response_model=ResultadoRefaccion)
def evaluar(solicitud: SolicitudRefaccion):
    resultado = evaluar_refaccion(
        elaborado=solicitud.elaborado,
        lleva_carne=solicitud.lleva_carne,
        base_pan=solicitud.base_pan,
        tortilla=solicitud.tortilla,
        ingredientes_disponibles=solicitud.ingredientes_disponibles,
    )
    return resultado