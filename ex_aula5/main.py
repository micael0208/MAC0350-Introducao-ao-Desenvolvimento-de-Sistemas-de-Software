from fastapi import FastAPI, Request, Depends, HTTPException, status, Cookie, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# --- Modelo de usuário ---
class User(BaseModel):
    username: str
    password: str
    bio: str

# "Banco" em memória
users_db: list[User] = []

# --- Página inicial (criar usuário) ---
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {}
    )


# --- Criar usuário ---
@app.post("/users")
async def create_user(request: Request):
    data = await request.json()

    user = User(
        username=data["username"],
        password=data["password"],
        bio=data["bio"]
    )

    users_db.append(user)
    return {"message": "Usuário criado com sucesso"}


# --- Página de login ---
@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(
        request,
        "login.html",
        {}
    )


# --- Login ---
@app.post("/login")
async def login(request: Request, response: Response):
    data = await request.json()

    username = data["username"]
    password = data["password"]

    user = next((u for u in users_db if u.username == username and u.password == password), None)

    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    response.set_cookie(key="session_user", value=username)
    return {"message": "Login realizado"}


# --- Dependência ---
def get_current_user(session_user: Annotated[str | None, Cookie()] = None):
    if not session_user:
        raise HTTPException(status_code=401, detail="Não logado")

    user = next((u for u in users_db if u.username == session_user), None)

    if not user:
        raise HTTPException(status_code=401, detail="Sessão inválida")

    return user


# --- Página protegida ---
@app.get("/home", response_class=HTMLResponse)
def profile(request: Request, user: User = Depends(get_current_user)):
    return templates.TemplateResponse(
        request,
        "profile.html",
        {
            "username": user.username,
            "bio": user.bio
        }
    )
