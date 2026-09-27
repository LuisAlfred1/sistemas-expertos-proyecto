from fastapi.testclient import TestClient
from backend.main import app


client = TestClient(app)


def test_r01_chiles_rellenos():
    response = client.post(
        "/api/v1/evaluar",
        json={
            "elaborado": True,
            "lleva_carne": True,
            "base_pan": False,
            "tortilla": False,
            "ingredientes_disponibles": []
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["refaccion_resultado"] == "Chiles Rellenos"
    assert data["regla"] == "R01-Ofrecer-Chiles-Rellenos"


def test_r02_ingredientes_insuficientes_elaborado():
    response = client.post(
        "/api/v1/evaluar",
        json={
            "elaborado": True,
            "lleva_carne": False,
            "base_pan": False,
            "tortilla": False,
            "ingredientes_disponibles": []
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["refaccion_resultado"] == "Ninguna"
    assert data["estado"] == "ingrediente_insuficientes"
    assert data["regla"] == "R02-Insuficientes-Elaborados"


def test_r03_shucos():
    response = client.post(
        "/api/v1/evaluar",
        json={
            "elaborado": False,
            "lleva_carne": False,
            "base_pan": True,
            "tortilla": False,
            "ingredientes_disponibles": []
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["refaccion_resultado"] == "Shucos"
    assert data["regla"] == "R03-Ofrecer-Shucos"


def test_r04_garnachas():
    response = client.post(
        "/api/v1/evaluar",
        json={
            "elaborado": False,
            "lleva_carne": False,
            "base_pan": False,
            "tortilla": True,
            "ingredientes_disponibles": []
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["refaccion_resultado"] == "Garnachas"
    assert data["regla"] == "R04-Ofrecer-Garnachas"


def test_r05_ingredientes_insuficientes_no_elaborado():
    response = client.post(
        "/api/v1/evaluar",
        json={
            "elaborado": False,
            "lleva_carne": False,
            "base_pan": False,
            "tortilla": False,
            "ingredientes_disponibles": []
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["refaccion_resultado"] == "Ninguna"
    assert data["estado"] == "ingrediente_insuficientes"
    assert data["regla"] == "R05-Insuficientes-No-Elaborados"
