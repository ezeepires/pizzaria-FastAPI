from fastapi import FastAPI

app = FastAPI()

from auth_routes import auth_router
from order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)

# para rodar o codigo, executar no terminal: uvicorn main:app --reload

# endpoint:
# /ordens (caminho)



# Rest APIs
# CRUD
# GET -> leitura/pegar
# POST -> enviar/criar
# PUT/PATCH -> editar
# DELETE -> deletar
