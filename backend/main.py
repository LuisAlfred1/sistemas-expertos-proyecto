from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from .modelos import SolicitudRefaccion, ResultadoRefaccion
from .motor_experto import evaluar_refaccion

# base_dir es la ruta absoluta del directorio raíz del proyecto. 
BASE_DIR = Path(__file__).resolve().parent.parent

# La ruta del directorio del frontend se construye a partir de la ruta base del proyecto.
FRONTEND_DIR = BASE_DIR / "frontend"

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

# Endpoint para evaluar la refacción
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


# Fronted
# Usamos la función `mount` para servir los archivos estáticos del frontend desde la ruta raíz ("/"). Esto permite que el frontend se cargue correctamente cuando se accede a la aplicación web.
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
