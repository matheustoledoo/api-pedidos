# api-pedidos — ATV04 (CRUD do serviço)

CRUD completo do recurso **Pedido**, em Python + FastAPI, respondendo com os códigos de status exigidos na atividade.

## Tabela de rotas

| Rota | Sucesso | Não existe | Entrada inválida |
|---|---|---|---|
| `POST /pedidos` | `201` + header `Location` | — | `422` |
| `GET /pedidos/{id}` | `200` | `404` | — |
| `PUT /pedidos/{id}` | `200` | `404` | `422` |
| `DELETE /pedidos/{id}` | `204` sem corpo | `404` | — |

## Como rodar

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Documentação interativa (Swagger): http://127.0.0.1:8000/docs

## Como testar

```bash
pytest -v
```

São 9 testes, um para cada célula da tabela acima.

### Testando na mão (curl)

```bash
# 201 + Location
curl -i -X POST http://127.0.0.1:8000/pedidos \
  -H "Content-Type: application/json" \
  -d '{"cliente":"Matheus","produto":"Teclado","quantidade":2,"preco":350}'

# 422 (quantidade negativa)
curl -i -X POST http://127.0.0.1:8000/pedidos \
  -H "Content-Type: application/json" \
  -d '{"cliente":"Matheus","produto":"Teclado","quantidade":-2,"preco":350}'

# 200
curl -i http://127.0.0.1:8000/pedidos/1

# 404
curl -i http://127.0.0.1:8000/pedidos/9999

# 200 (update)
curl -i -X PUT http://127.0.0.1:8000/pedidos/1 \
  -H "Content-Type: application/json" \
  -d '{"cliente":"Matheus","produto":"Teclado","quantidade":10,"preco":350}'

# 204 sem corpo
curl -i -X DELETE http://127.0.0.1:8000/pedidos/1

# 404 no delete repetido
curl -i -X DELETE http://127.0.0.1:8000/pedidos/1
```

## Decisões

- **Armazenamento em memória** (dicionário), sem banco — o escopo da atividade é o contrato HTTP, não persistência.
- **422 vem do Pydantic**: as restrições (`min_length`, `gt=0`, tipos) fazem o FastAPI devolver 422 antes de chegar na função.
- **204 com `Response` explícito** para garantir corpo realmente vazio, como manda a RFC 9110.
- `GET /pedidos` (listagem) foi incluído como extra, fora das quatro rotas exigidas.
