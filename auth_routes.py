from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["auth"])
# dominio/auth/ - para manter ordem e organizacao

@auth_router.get("/")
async def autenticar():
    """
    Essa e a rota padrao de autenticacao do nosso sistema
    """ 
    # Isso acima e chamado de comentarios para APIs
    return {"mensagem": "Voce acessou a rota padrao de autenticacao", "autenticado": False}

