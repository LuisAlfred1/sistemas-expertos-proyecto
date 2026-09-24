from pathlib import Path
import clips

def evaluar_refaccion(
        elaborado: bool,
        lleva_carne: bool,
        base_pan: bool,
        tortilla: bool,
        ingredientes_disponibles: list[str],
) -> dict:

    ruta_clp = Path(__file__).resolve().parent / "conocimiento.clp"

    env = clips.Environment()
    env.load(str(ruta_clp))

    preparacion_template = env.find_template("preparacion")

    preparacion_template.assert_fact(
        elaborado=clips.Symbol("si" if elaborado else "no"),
        lleva_carne=clips.Symbol("si" if lleva_carne else "no"),
        base_pan=clips.Symbol("si" if base_pan else "no"),
        tortilla=clips.Symbol("si" if tortilla else "no"),
    )

    env.run()

    # Para imprimir si esta obteniendo la informacion correcta
    print("Motor ejecutado")

    resultado_template = env.find_template("resultado")
    resultados = list(resultado_template.facts())

    # Para imprimir si esta obteniendo la informacion correcta
    print("Resultados:", resultados)

    if not resultados:
        return {
            "estado": "error",
            "refaccion_resultado": None,
            "mensaje": "No se pudo determinar una refacción guatemalteca.",
            "justificacion": None,
            "regla": None,
        }

    fact = resultados[0]

    preparacion = str(fact["preparacion"])

    if preparacion == "Ninguna":
        estado = "ingrediente_insuficientes"
    else:
        estado = "exito"

    # Para imprimir si esta obteniendo la informacion correcta
    print("Preparacion:", preparacion)
    print("Estado:", estado)
    
    return {
        "estado": estado,
        "refaccion_resultado": preparacion,
        "mensaje": str(fact["mensaje"]),
        "justificacion": str(fact["justificacion"]),
        "regla": str(fact["regla"]),
    }