from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from schemas import PedidoSchema, ItemPedidoSchema
from models import Pedido, Usuario, ItemPedido

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"], dependencies=[Depends(verificar_token)])
# dominio/pedidos/  ->   para manter ordem e organizacao

@order_router.get("/")
async def pedidos():
    """
    Essa e a rota padrao de pedidos do nosso sistema. Todas as rotas dos pedidos precisam de autenticacao
    """
    # Isso acima e chamado de comentarios para APIs
    return {"mensagem": "Voce acessou a rota de pedidos"}

# dominio/pedidos/pedido
@order_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    """
    Essa e a rota padrao de criacao de pedidos
    """
    novo_pedido = Pedido(usuario=pedido_schema.id_usuario)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem": f"Pedido criado com sucesso. ID do pedido: {novo_pedido.id}"}

# gostei dessa rota, otima logica!
@order_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido nao encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Voce nao tem autorizacao para fazer essa modificacao")
    pedido.status = "CANCELADO"
    session.commit()
    return {
        "mensagem": f"Pedido com id: {pedido.id} cancelado com sucesso",
        "pedido": pedido
    }

@order_router.get("/listar")
async def listar_pedidos(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Voce nao tem autorizacao para fazer essa operacao")
    else:
        pedidos = session.query(Pedido).all()
        return {
            "pedidos": pedidos
        }
    
# so pode adicionar coisas no pedido quem e o dono do pedido
# ou uqme e admin
@order_router.post("/pedido/adicionar-item/{id_pedido}")
async def adicionar_item_pedido(
                id_pedido: int,
                item_pedido_schema: ItemPedidoSchema, 
                session: Session = Depends(pegar_sessao), 
                usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido nao existente")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Voce nao tem autorizacao para fazer essa operacao")
    item_pedido = ItemPedido(item_pedido_schema.quantidade, 
                             item_pedido_schema.sabor, 
                             item_pedido_schema.tamanho,
                             item_pedido_schema.preco_unitario,
                             id_pedido)
    pedido.calcular_preco()
    session.add(item_pedido)
    session.commit()
    return {
        "mensagem": "Item criado com sucesso",
        "item_id": item_pedido.id,
        "preco_pedido": pedido.preco
    }
