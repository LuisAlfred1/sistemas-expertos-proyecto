import pytest

from backend.motor_experto import (
    evaluar_recomendacion,
    obtener_opciones,
)


# Reutilizable para acceder al motor de recomendaciones.
@pytest.fixture
def motor():
    return evaluar_recomendacion


# Verifica que el sistema exponga las categorías e ingredientes esperados.
def test_opciones_disponibles(
    motor
):

    opciones = obtener_opciones()

    # Las categorías deben seguir la estructura definida por el dominio.
    assert set(opciones["categorias"]) == {
        "antojito",
        "plato_fuerte",
        "postre",
    }

    # Cada categoría debe tener una colección de ingredientes propia.
    assert set(opciones["ingredientes_por_categoria"]) == set(
        opciones["categorias"]
    )

    # Se comprueba la presencia de algunos ingredientes clave.
    assert "pollo" in opciones["ingredientes"]
    assert "tortilla" in opciones["ingredientes"]
    assert "platano" in opciones["ingredientes"]


# Si la categoría y el ingrediente coinciden exactamente, debe devolver un resultado de éxito.
def test_coincidencia_exacta(
    motor
):

    resultado = motor(
        "antojito",
        "tortilla",
    )

    assert resultado["estado"] == "exito"

    # La coincidencia exacta debe devolver solo los platillos que cumplen con ambas condiciones.
    assert {
        recomendacion["platillo"]
        for recomendacion in resultado["recomendaciones"]
    } == {
        "Tostadas de guacamol",
        "Garnachas",
    }

    # Cada recomendación debe incluir el nivel, puntaje y regla esperados.
    for recomendacion in resultado["recomendaciones"]:

        assert recomendacion["nivel"] == "exacta"
        assert recomendacion["puntaje"] == 100
        assert recomendacion["regla"] == "R01-Coincidencia-Exacta"


# Cuando se indica solo una categoría válida, el motor debe sugerir platillos por categoría.
def test_recomendacion_categoria(
    motor
):

    resultado = motor(
        "plato_fuerte",
        "cualquiera",
    )

    assert resultado["estado"] == "exito"

    # El primer resultado debe corresponder al platillo dominante para la categoría solicitada.
    assert (
        resultado["recomendaciones"][0]["platillo"]
        == "Pollo guisado"
    )

    assert (
        resultado["recomendaciones"][0]["nivel"]
        == "categoria"
    )

    assert (
        resultado["recomendaciones"][0]["regla"]
        == "R02-Solo-Categoria"
    )


# Si se busca un ingrediente sin especificar categoría, debe encontrar coincidencias por ingrediente.
def test_recomendacion_ingrediente(
    motor
):

    resultado = motor(
        "cualquiera",
        "canela",
    )

    assert resultado["estado"] == "exito"

    # Se esperan los platillos que contienen el ingrediente indicado.
    assert {
        recomendacion["platillo"]
        for recomendacion in resultado["recomendaciones"]
    } == {
        "Platanos en mole",
        "Rellenitos de platano",
    }

    # Las recomendaciones deben registrarse como coincidencia por ingrediente.
    for recomendacion in resultado["recomendaciones"]:

        assert recomendacion["nivel"] == "ingrediente"
        assert recomendacion["regla"] == "R03-Solo-Ingrediente"


# Cuando la categoría y el ingrediente no coinciden de forma exacta, se devuelven alternativas con puntaje menor.
def test_recomendaciones_alternativas(
    motor
):

    resultado = motor(
        "antojito",
        "pollo",
    )

    assert resultado["estado"] == "alternativas"

    # Se extrae un mapa de platillos para validar cada alternativa individualmente.
    recomendaciones = {
        recomendacion["platillo"]: recomendacion
        for recomendacion in resultado["recomendaciones"]
    }

    assert set(recomendaciones) == {
        "Tostadas de guacamol",
        "Garnachas",
        "Shucos",
        "Pollo guisado",
    }

    # Las alternativas comparten una puntuación y nivel comunes.
    for recomendacion in recomendaciones.values():

        assert recomendacion["nivel"] == "alternativa"
        assert recomendacion["puntaje"] == 50

    # Cada alternativa debe indicar la regla específica que la generó.
    assert (
        recomendaciones["Garnachas"]["regla"]
        == "R04-Alternativa-Por-Categoria"
    )

    assert (
        recomendaciones["Pollo guisado"]["regla"]
        == "R05-Alternativa-Por-Ingrediente"
    )


# La categoría debe pertenecer a un conjunto válido; cualquier otra debe lanzar un error.
def test_categoria_invalida(
    motor
):

    with pytest.raises(ValueError):

        motor(
            "comida",
            "tortilla",
        )


# Los ingredientes no registrados deben rechazarse con una excepción.
def test_ingrediente_invalido(
    motor
):

    with pytest.raises(ValueError):

        motor(
            "antojito",
            "pizza",
        )


# La selección "cualquiera" para ambos campos no es válida porque debe haber al menos un criterio real.
def test_seleccion_invalida(
    motor
):

    with pytest.raises(ValueError):

        motor(
            "cualquiera",
            "cualquiera",
        )