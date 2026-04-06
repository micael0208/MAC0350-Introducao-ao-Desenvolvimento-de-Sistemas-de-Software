from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Lista em memória
users = []

# Permitir HTMX funcionar tranquilo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- 1. GET / -> retorna HTML ---
@app.get("/", response_class=HTMLResponse)
async def home():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()


# --- 2. POST /users -> adiciona usuário ---
@app.post("/users")
async def add_user(request: Request):
    data = await request.json()

    nome = data.get("nome")
    idade = data.get("idade")

    user = {
        "nome": nome,
        "idade": idade
    }

    users.append(user)

    return JSONResponse(content={"Usuário adicionado": users})


# --- 3. GET /users -> lista ou índice ---
@app.get("/users")
async def get_users(index: int = None):
    if index is not None:
        if 0 <= index < len(users):
            return JSONResponse(content=users[index])
        else:
            return JSONResponse(content={"erro": "Índice inválido"})
    
    return JSONResponse(content=users)


# --- 4. DELETE /users -> limpa lista ---
@app.delete("/users")
async def delete_users():
    users.clear()
    return JSONResponse(content={"mensagem": "Todos os usuários foram removidos"})
