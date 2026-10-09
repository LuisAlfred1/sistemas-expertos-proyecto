from pathlib import Path

import clips

RUTA_CLP = Path(__file__).resolve().parent / "conocimientoV2.clp"


def _nuevo_entorno() -> clips.Environment:
    env = clips.Environment()
    env.load(str(RUTA_CLP))
    # IMPORTANTE: reset() carga los (deffacts) con los platillos.
    # Antes no hacía falta porque el .clp no tenía hechos; ahora sí.
    env.reset()
    return env


def _a_python(valor):
    if isinstance(valor, (list, tuple)):
        return [_a_python(v) for v in valor]
    if isinstance(valor, clips.Symbol):
        return str(valor)
    return valor


def _hechos(env: clips.Environment, plantilla: str) -> list[dict]:
    tpl = env.find_template(plantilla)
    return [{k: _a_python(v) for k, v in dict(f).items()} for f in tpl.facts()]


def obtener_opciones() -> dict:
    """Categorías e ingredientes leídos de la base de conocimiento."""
    platillos = _hechos(_nuevo_entorno(), "platillo")
    return {
        "categorias": sorted({p["categoria"] for p in platillos}),
        "ingredientes": sorted({i for p in platillos for i in p["ingredientes"]}),
    }


def evaluar_recomendacion(categoria: str, ingrediente: str) -> dict:
    """
    Ejecuta el motor CLIPS. Lanza ValueError si la entrada no es válida.
    Devuelve un dict compatible con ResultadoRecomendacion.
    """
    opciones = obtener_opciones()

    if categoria != "cualquiera" and categoria not in opciones["categorias"]:
        raise ValueError("Categoría no válida")
    if ingrediente != "cualquiera" and ingrediente not in opciones["ingredientes"]:
        raise ValueError("Ingrediente no válido")
    if categoria == "cualquiera" and ingrediente == "cualquiera":
        raise ValueError("Elige al menos una categoría o un ingrediente")

    env = _nuevo_entorno()

    # assert_fact con la plantilla: no se arma ningún string de CLIPS con texto del usuario
    env.find_template("solicitud").assert_fact(
        categoria=clips.Symbol(categoria),
        ingrediente=clips.Symbol(ingrediente),
    )
    env.run()

    # Para depurar si está obteniendo la información correcta
    print("Motor ejecutado")

    platillos = {p["nombre"]: p for p in _hechos(env, "platillo")}
    resultados = _hechos(env, "recomendacion")
    print("Resultados:", resultados)

    if not resultados:
        return {
            "estado": "error",
            "mensaje": "No se pudo determinar una recomendación.",
            "recomendaciones": [],
        }

    # Un platillo puede salir por varias reglas (R04 y R05): dejamos el mejor puntaje
    mejores: dict[str, dict] = {}
    for r in resultados:
        actual = mejores.get(r["platillo"])
        if actual is None or r["puntaje"] > actual["puntaje"]:
            mejores[r["platillo"]] = r

    ordenados = sorted(mejores.values(), key=lambda r: -r["puntaje"])

    if ordenados[0]["nivel"] == "ninguna":
        return {
            "estado": "sin_resultado",
            "mensaje": ordenados[0]["justificacion"],
            "recomendaciones": [],
        }

    recomendaciones = []
    for r in ordenados:
        p = platillos.get(r["platillo"], {})
        recomendaciones.append(
            {
                "platillo": r["platillo"],
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

    hay_alternativa = ordenados[0]["nivel"] == "alternativa"
    return {
        "estado": "alternativas" if hay_alternativa else "exito",
        "mensaje": (
            "No hay una coincidencia exacta, pero estas opciones podrían gustarte."
            if hay_alternativa
            else "Estas son nuestras recomendaciones."
        ),
        "recomendaciones": recomendaciones,
    }
