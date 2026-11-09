import pytest

from backend.motor_experto import (
    evaluar_recomendacion,
    obtener_opciones,
)


# Devuelve la función principal del motor experto para reutilizarla
# en todas las pruebas sin repetir la importación ni la inicialización.
@pytest.fixture
def motor():
    return evaluar_recomendacion


# Prueba de validación del catálogo de datos del sistema.
# Verifica que el motor exponga exactamente las categorías permitidas y que cada una
# tenga su conjunto correspondiente de ingredientes disponibles.
def test_opciones_disponibles(
    motor
):

    opciones = obtener_opciones()

    # Se espera que solo existan tres categorías dentro del dominio del problema.
    assert set(opciones["categorias"]) == {
        "antojito",
        "plato_fuerte",
        "postre",
    }

    # El diccionario de ingredientes por categoría debe contener una llave por cada
    # categoría registrada, para asegurar que el catálogo esté completo y consistente.
    assert set(opciones["ingredientes_por_categoria"]) == set(
        opciones["categorias"]
    )

    # Se validan algunos ingredientes representativos que deben estar presentes en
    # el vocabulario global para que el motor pueda hacer coincidencias reales.
    assert "pollo" in opciones["ingredientes"]
    assert "tortilla" in opciones["ingredientes"]
    assert "platano" in opciones["ingredientes"]


# Caso base de éxito: cuando la categoría y el ingrediente coinciden exactamente,
# el sistema debe devolver únicamente los platillos que cumplen ambas condiciones,
# con nivel de coincidencia exacta y puntaje máximo.
def test_coincidencia_exacta(
    motor
):

    resultado = motor(
        "antojito",
        "tortilla",
    )

    # El estado de la recomendación debe indicar éxito completo, no una alternativa.
    assert resultado["estado"] == "exito"

    # La coincidencia exacta debe filtrar solo las opciones que cumplen con la
    # categoría y el ingrediente solicitados exactamente.
    assert {
        recomendacion["platillo"]
        for recomendacion in resultado["recomendaciones"]
    } == {
        "Tostadas de guacamol",
        "Garnachas",
    }

    # Cada una de las recomendaciones exactas debe estar marcada con la regla y el
    # puntaje definidos en la especificación del motor.
    for recomendacion in resultado["recomendaciones"]:

        assert recomendacion["nivel"] == "exacta"
        assert recomendacion["puntaje"] == 100
        assert recomendacion["regla"] == "R01-Coincidencia-Exacta"


# Prueba de recomendación por categoría.
# Cuando no se especifica un ingrediente, el sistema debe inferir platillos según la
# categoría indicada y devolver la recomendación más relevante para esa clase.
def test_recomendacion_categoria(
    motor
):

    resultado = motor(
        "plato_fuerte",
        "cualquiera",
    )

    # Este caso debe considerarse como una recomendación exitosa, aunque no exista
    # una coincidencia exacta con ingredientes.
    assert resultado["estado"] == "exito"

    # El primer elemento de la lista debe ser el platillo principal asociado a la
    # categoría elegida según la prioridad de las reglas del motor.
    assert (
        resultado["recomendaciones"][0]["platillo"]
        == "Pollo guisado"
    )

    # La recomendación por categoría tiene un nivel explícito y usa una regla de
    # clasificación distinta a la coincidencia exacta.
    assert (
        resultado["recomendaciones"][0]["nivel"]
        == "categoria"
    )

    assert (
        resultado["recomendaciones"][0]["regla"]
        == "R02-Solo-Categoria"
    )


# Prueba de recomendación por ingrediente.
# Cuando se ingresa un ingrediente sin categoría, el motor debe buscar platillos que lo
# contengan en sus ingredientes, aun si no se especifica una clase concreta.
def test_recomendacion_ingrediente(
    motor
):

    resultado = motor(
        "cualquiera",
        "canela",
    )

    # El sistema debe considerar la solicitud válida y devolver resultados que
    # correspondan a la coincidencia del ingrediente.
    assert resultado["estado"] == "exito"

    # Se esperan exactamente los platillos asociados con la canela, sin incluir otros
    # elementos que no coincidan con el criterio solicitado.
    assert {
        recomendacion["platillo"]
        for recomendacion in resultado["recomendaciones"]
    } == {
        "Platanos en mole",
        "Rellenitos de platano",
    }

    # Cada recomendación debe indicar que la relación se hizo por ingrediente y no por
    # categoría ni por coincidencia completa.
    for recomendacion in resultado["recomendaciones"]:

        assert recomendacion["nivel"] == "ingrediente"
        assert recomendacion["regla"] == "R03-Solo-Ingrediente"


# Prueba de alternativas parciales.
# Cuando la categoría y el ingrediente no son completamente compatibles, el sistema
# debe devolver opciones alternativas con una penalización en puntaje y con reglas
# específicas para cada tipo de relación indirecta.
def test_recomendaciones_alternativas(
    motor
):

    resultado = motor(
        "antojito",
        "pollo",
    )

    # Este caso no es un éxito exacto, pero tampoco un error: el motor debe devolver
    # un estado de alternativas que muestre opciones cercanas a la solicitud.
    assert resultado["estado"] == "alternativas"

    # Se convierte la lista de recomendaciones a un diccionario para comparar cada
    # platillo y validar el contenido de su metadata de forma más precisa.
    recomendaciones = {
        recomendacion["platillo"]: recomendacion
        for recomendacion in resultado["recomendaciones"]
    }

    # Se espera una combinación de resultados que responden a la categoría y al
    # ingrediente de forma indirecta, pero no exacta.
    assert set(recomendaciones) == {
        "Tostadas de guacamol",
        "Garnachas",
        "Shucos",
        "Pollo guisado",
    }

    # Todas las alternativas deben compartir el mismo nivel y el mismo puntaje
    # reducido para indicar que son sugerencias parciales y no coincidencias completas.
    for recomendacion in recomendaciones.values():

        assert recomendacion["nivel"] == "alternativa"
        assert recomendacion["puntaje"] == 50

    # Cada alternativa debe documentar la razón específica por la cual fue incluida,
    # ya sea por categoría o por ingrediente.
    assert (
        recomendaciones["Garnachas"]["regla"]
        == "R04-Alternativa-Por-Categoria"
    )

    assert (
        recomendaciones["Pollo guisado"]["regla"]
        == "R05-Alternativa-Por-Ingrediente"
    )


# Prueba de validación de entrada.
# Si la categoría no pertenece al catálogo del sistema, el motor debe rechazarla con
# una excepción explicita en vez de devolver una recomendación inválida.
def test_categoria_invalida(
    motor
):

    with pytest.raises(ValueError):

        motor(
            "comida",
            "tortilla",
        )


# Prueba de validación del ingrediente.
# Si el ingrediente no existe en el conjunto de datos, el sistema debe fallar con
# ValueError para evitar sugerencias inconsistentes o vacías.
def test_ingrediente_invalido(
    motor
):

    with pytest.raises(ValueError):

        motor(
            "antojito",
            "pizza",
        )


# Prueba de validación de criterio de entrada.
# La combinación "cualquiera" con "cualquiera" no es un caso válido porque el motor
# necesita al menos una condición útil para generar una recomendación.
def test_seleccion_invalida(
    motor
):

    with pytest.raises(ValueError):

        motor(
            "cualquiera",
            "cualquiera",
        )