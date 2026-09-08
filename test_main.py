"""
Testes que provam a tabela de códigos da ATV04.
Rodar com:  pytest -v
"""

import pytest
from fastapi.testclient import TestClient

import main
from main import app

client = TestClient(app)

PEDIDO_VALIDO = {
    "cliente": "Matheus",
    "produto": "Teclado mecânico",
    "quantidade": 2,
    "preco": 350.00,
}

PEDIDO_INVALIDO = {
    "cliente": "",          # min_length=1
    "produto": "Mouse",
    "quantidade": -5,       # gt=0
    "preco": "abc",         # não é número
}


@pytest.fixture(autouse=True)
def limpar_estado():
    """Cada teste começa com o armazenamento zerado."""
    main.pedidos.clear()
    main.proximo_id = 1
    yield


def criar() -> int:
    return client.post("/pedidos", json=PEDIDO_VALIDO).json()["id"]


# ------------------------------- POST --------------------------------------
def test_post_retorna_201_e_location():
    r = client.post("/pedidos", json=PEDIDO_VALIDO)
    assert r.status_code == 201
    assert r.headers["Location"] == f"/pedidos/{r.json()['id']}"


def test_post_invalido_retorna_422():
    assert client.post("/pedidos", json=PEDIDO_INVALIDO).status_code == 422


# ------------------------------- GET ---------------------------------------
def test_get_existente_retorna_200():
    pedido_id = criar()
    r = client.get(f"/pedidos/{pedido_id}")
    assert r.status_code == 200
    assert r.json()["cliente"] == "Matheus"


def test_get_inexistente_retorna_404():
    assert client.get("/pedidos/9999").status_code == 404


# ------------------------------- PUT ---------------------------------------
def test_put_existente_retorna_200():
    pedido_id = criar()
    novo = {**PEDIDO_VALIDO, "quantidade": 10}
    r = client.put(f"/pedidos/{pedido_id}", json=novo)
    assert r.status_code == 200
    assert r.json()["quantidade"] == 10


def test_put_inexistente_retorna_404():
    assert client.put("/pedidos/9999", json=PEDIDO_VALIDO).status_code == 404


def test_put_invalido_retorna_422():
    pedido_id = criar()
    assert client.put(f"/pedidos/{pedido_id}", json=PEDIDO_INVALIDO).status_code == 422


# ------------------------------ DELETE -------------------------------------
def test_delete_existente_retorna_204_sem_corpo():
    pedido_id = criar()
    r = client.delete(f"/pedidos/{pedido_id}")
    assert r.status_code == 204
    assert r.content == b""
    assert client.get(f"/pedidos/{pedido_id}").status_code == 404


def test_delete_inexistente_retorna_404():
    assert client.delete("/pedidos/9999").status_code == 404
