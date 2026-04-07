from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao
from main import bcrypt_context
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix="/auth", tags=["auth"])
# dominio/auth/ - para manter ordem e organizacao

def criar_token(id):
    token = f"sbfbsauiehbdlks{id}"
    return token

@auth_router.get("/")
async def home():
    """
    Essa e a rota padrao de autenticacao do nosso sistema
    """ 
    # Isso acima e chamado de comentarios para APIs
    return {"mensagem": "Voce acessou a rota padrao de autenticacao", "autenticado": False}

@auth_router.post("/criar_conta")
async def criar_conta(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first()
    if usuario:
        # Ja existe um usuario com esse email
        raise HTTPException(status_code=400, detail="email do usuario ja cadastrado")
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada, usuario_schema.ativo, usuario_schema.admin)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": f"usuario cadastrado com sucesso {usuario_schema.email}"}

# login -> email e senha -> Token JWT (Json Web Token) fdgsdfdsf544dsdsas545dfsdf54f44f5g5
@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email==login_schema.email).first()
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario nao encontrado")
    else:
        access_token = criar_token(usuario.id)
        return {
            "access_token": access_token,
            "token_type": "Bearer"
            }
        # JWT Bearner

        # headers = {"Access-Token": "Bearer token"}