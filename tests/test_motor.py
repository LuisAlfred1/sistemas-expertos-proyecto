import pytest

from backend.motor_experto import (
    evaluar_recomendacion,
    obtener_opciones,
)


@pytest.fixture
def motor():
    return evaluar_recomendacion


def test_opciones_disponibles(
    motor
):

    opciones = obtener_opciones()

    assert set(opciones["categorias"]) == {
        "antojito",
        "plato_fuerte",
        "postre",
    }

    assert set(opciones["ingredientes_por_categoria"]) == set(
        opciones["categorias"]
    )

    assert "pollo" in opciones["ingredientes"]
    assert "tortilla" in opciones["ingredientes"]
    assert "platano" in opciones["ingredientes"]


def test_coincidencia_exacta(
    motor
):

    resultado = motor(
        "antojito",
        "tortilla",
    )

    assert resultado["estado"] == "exito"

    assert {
        recomendacion["platillo"]
        for recomendacion in resultado["recomendaciones"]
    } == {
        "Tostadas de guacamol",
        "Garnachas",
    }

    for recomendacion in resultado["recomendaciones"]:

        assert recomendacion["nivel"] == "exacta"
        assert recomendacion["puntaje"] == 100
        assert recomendacion["regla"] == "R01-Coincidencia-Exacta"


def test_recomendacion_categoria(
    motor
):

    resultado = motor(
        "plato_fuerte",
        "cualquiera",
    )

    assert resultado["estado"] == "exito"

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


def test_recomendacion_ingrediente(
    motor
):

    resultado = motor(
        "cualquiera",
        "canela",
    )

    assert resultado["estado"] == "exito"

    assert {
        recomendacion["platillo"]
        for recomendacion in resultado["recomendaciones"]
    } == {
        "Platanos en mole",
        "Rellenitos de platano",
    }

    for recomendacion in resultado["recomendaciones"]:

        assert recomendacion["nivel"] == "ingrediente"
        assert recomendacion["regla"] == "R03-Solo-Ingrediente"


def test_recomendaciones_alternativas(
    motor
):

    resultado = motor(
        "antojito",
        "pollo",
    )

    assert resultado["estado"] == "alternativas"

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

    for recomendacion in recomendaciones.values():

        assert recomendacion["nivel"] == "alternativa"
        assert recomendacion["puntaje"] == 50

    assert (
        recomendaciones["Garnachas"]["regla"]
        == "R04-Alternativa-Por-Categoria"
    )

    assert (
        recomendaciones["Pollo guisado"]["regla"]
        == "R05-Alternativa-Por-Ingrediente"
    )


def test_categoria_invalida(
    motor
):

    with pytest.raises(ValueError):

        motor(
            "comida",
            "tortilla",
        )


def test_ingrediente_invalido(
    motor
):

    with pytest.raises(ValueError):

        motor(
            "antojito",
            "pizza",
        )


def test_seleccion_invalida(
    motor
):

    with pytest.raises(ValueError):

        motor(
            "cualquiera",
            "cualquiera",
        )