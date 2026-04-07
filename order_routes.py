from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import pegar_sessao
from schemas import PedidoSchema
from models import Pedido

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"])
# dominio/pedidos/  ->   para manter ordem e organizacao

@order_router.get("/lista")
async def pedidos():
    """
    Essa e a rota padrao de pedidos do nosso sistema. Todas as rotas dos pedidos precisam de autenticacao
    """
    # Isso acima e chamado de comentarios para APIs
    return {"mensagem":"Voce acessou a rota de pedidos"}

# dominio/pedidos/pedido
@order_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    """
    Essa e a rota padrao de criacao de pedidos
    """
    novo_pedido = Pedido(usuario=pedido_schema.usuario)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem": f"Pedido criado com sucesso. ID do pedido: {novo_pedido.id}"}
