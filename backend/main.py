"""
Backend del recomendador: FastAPI + CLIPS (clipspy)

Instalar:  pip install fastapi uvicorn clipspy
Ejecutar:  uvicorn main:app --reload
"""

from pathlib import Path

import clips
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

RUTA_CLP = str(Path(__file__).parent / "conocimientoV2.clp")

app = FastAPI(title="Recomendador del comedor")

# Ajusta los origenes a donde sirvas tu frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def nuevo_entorno() -> clips.Environment:
    """Un entorno limpio por consulta (evita mezclar hechos entre usuarios)."""
    env = clips.Environment()
    env.load(RUTA_CLP)
    env.reset()  # carga los deffacts (platillos)
    return env


def a_python(valor):
    if isinstance(valor, (list, tuple)):
        return [a_python(v) for v in valor]
    if isinstance(valor, clips.Symbol):
        return str(valor)
    return valor


def hechos_de(env: clips.Environment, plantilla: str) -> list[dict]:
    return [
        {k: a_python(v) for k, v in dict(f).items()}
        for f in env.facts()
        if f.template.name == plantilla
    ]


def catalogo() -> dict:
    """Categorias e ingredientes disponibles, leidos de la base de conocimiento."""
    platillos = hechos_de(nuevo_entorno(), "platillo")
    categorias = sorted({p["categoria"] for p in platillos})
    ingredientes = sorted({i for p in platillos for i in p["ingredientes"]})
    return {"categorias": categorias, "ingredientes": ingredientes}


class Consulta(BaseModel):
    categoria: str = "cualquiera"
    ingrediente: str = "cualquiera"


@app.get("/api/opciones")
def opciones():
    return catalogo()


@app.post("/api/recomendar")
def recomendar(consulta: Consulta):
    cat = catalogo()

    # Validar contra la lista blanca (nunca construimos strings de CLIPS con texto del usuario)
    if (
        consulta.categoria != "cualquiera"
        and consulta.categoria not in cat["categorias"]
    ):
        raise HTTPException(422, "Categoria no valida")
    if (
        consulta.ingrediente != "cualquiera"
        and consulta.ingrediente not in cat["ingredientes"]
    ):
        raise HTTPException(422, "Ingrediente no valido")
    if consulta.categoria == "cualquiera" and consulta.ingrediente == "cualquiera":
        raise HTTPException(400, "Elige al menos una categoria o un ingrediente")

    env = nuevo_entorno()
    env.find_template("solicitud").assert_fact(
        categoria=clips.Symbol(consulta.categoria),
        ingrediente=clips.Symbol(consulta.ingrediente),
    )
    env.run()

    platillos = {p["nombre"]: p for p in hechos_de(env, "platillo")}

    # Un platillo puede salir por varias reglas: nos quedamos con el mejor puntaje
    mejores: dict[str, dict] = {}
    for r in hechos_de(env, "recomendacion"):
        actual = mejores.get(r["platillo"])
        if actual is None or r["puntaje"] > actual["puntaje"]:
            mejores[r["platillo"]] = r

    resultados = []
    for nombre, r in sorted(mejores.items(), key=lambda kv: -kv[1]["puntaje"]):
        p = platillos.get(nombre, {})
        resultados.append(
            {
                "platillo": nombre,
                "nivel": r["nivel"],
                "puntaje": r["puntaje"],
                "mensaje": r["mensaje"],
                "justificacion": r["justificacion"],
                "regla": r["regla"],
                "categoria": p.get("categoria"),
                "sabor": p.get("sabor"),
                "descripcion": p.get("descripcion"),
                "porciones": p.get("porciones"),
                "pagina": p.get("pagina"),
            }
        )

    return {"consulta": consulta, "resultados": resultados}
