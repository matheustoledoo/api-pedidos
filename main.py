"""
ATV04 - CRUD do serviço api-pedidos
Desenvolvimento de APIs (REST, SOA) - Aula 3

Rotas e códigos de status exigidos:
    POST   /pedidos        -> 201 + header Location | 422 entrada inválida
    GET    /pedidos/{id}   -> 200 | 404 não existe
    PUT    /pedidos/{id}   -> 200 | 404 não existe | 422 entrada inválida
    DELETE /pedidos/{id}   -> 204 sem corpo | 404 não existe
"""

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="api-pedidos",
    description="CRUD do recurso Pedido - ATV04",
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# Armazenamento em memória (sem banco de dados, conforme escopo da atividade)
# ---------------------------------------------------------------------------
pedidos: dict[int, dict] = {}
proximo_id: int = 1


# ---------------------------------------------------------------------------
# Modelos (o Pydantic é quem devolve 422 automaticamente na entrada inválida)
# ---------------------------------------------------------------------------
class PedidoEntrada(BaseModel):
    cliente: str = Field(min_length=1, max_length=120)
    produto: str = Field(min_length=1, max_length=120)
    quantidade: int = Field(gt=0)
    preco: float = Field(gt=0)


class PedidoSaida(PedidoEntrada):
    id: int


# ---------------------------------------------------------------------------
# CREATE -> 201 + Location
# ---------------------------------------------------------------------------
@app.post(
    "/pedidos",
    response_model=PedidoSaida,
    status_code=status.HTTP_201_CREATED,
)
def criar_pedido(pedido: PedidoEntrada, response: Response):
    global proximo_id

    novo = {"id": proximo_id, **pedido.model_dump()}
    pedidos[proximo_id] = novo
    proximo_id += 1

    # O recurso criado precisa ser localizável: header Location
    response.headers["Location"] = f"/pedidos/{novo['id']}"
    return novo


# ---------------------------------------------------------------------------
# READ -> 200 | 404
# ---------------------------------------------------------------------------
@app.get("/pedidos/{pedido_id}", response_model=PedidoSaida)
def buscar_pedido(pedido_id: int):
    pedido = pedidos.get(pedido_id)
    if pedido is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pedido {pedido_id} não encontrado",
        )
    return pedido


# ---------------------------------------------------------------------------
# UPDATE -> 200 | 404 | 422
# ---------------------------------------------------------------------------
@app.put("/pedidos/{pedido_id}", response_model=PedidoSaida)
def atualizar_pedido(pedido_id: int, pedido: PedidoEntrada):
    if pedido_id not in pedidos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pedido {pedido_id} não encontrado",
        )

    atualizado = {"id": pedido_id, **pedido.model_dump()}
    pedidos[pedido_id] = atualizado
    return atualizado


# ---------------------------------------------------------------------------
# DELETE -> 204 sem corpo | 404
# ---------------------------------------------------------------------------
@app.delete("/pedidos/{pedido_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_pedido(pedido_id: int):
    if pedido_id not in pedidos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pedido {pedido_id} não encontrado",
        )

    del pedidos[pedido_id]
    # Response explícito garante corpo vazio de verdade no 204
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ---------------------------------------------------------------------------
# Extra (não exigido): listagem, útil para demonstrar em sala
# ---------------------------------------------------------------------------
@app.get("/pedidos", response_model=list[PedidoSaida])
def listar_pedidos():
    return list(pedidos.values())
