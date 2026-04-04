from fastapi import APIRouter

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"])
# dominio/pedidos/  ->   para manter ordem e organizacao

@order_router.get("/lista")
async def pedidos():
    """
    Essa e a rota padrao de pedidos do nosso sistema. Todas as rotas dos pedidos precisam de autenticacao
    """
    # Isso acima e chamado de comentarios para APIs
    return {"mensagem":"Voce acessou a rota de pedidos"}

