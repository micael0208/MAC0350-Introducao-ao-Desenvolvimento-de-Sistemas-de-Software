# Arquivo main.py

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from Models import Aluno
from contextlib import asynccontextmanager
from sqlmodel import SQLModel, create_engine, Session, select

@asynccontextmanager
async def initFunction(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=initFunction)

arquivo_sqlite = "HTMX2.db"
url_sqlite = f"sqlite:///{arquivo_sqlite}"

engine = create_engine(url_sqlite)

templates = Jinja2Templates(directory="Templates")

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
 
    
@app.get("/busca", response_class=HTMLResponse)
def busca(request: Request):
    return templates.TemplateResponse(request, "index.html", {})

@app.get("/lista", response_class=HTMLResponse)
def lista(request: Request, busca: str = '', page: int = 1):
    limite = 5
    offset = (page - 1) * limite

    with Session(engine) as session:
        query = select(Aluno)

        if busca:
            query = query.where(Aluno.nome.contains(busca))

        total = session.exec(query).all()

        alunos = session.exec(
            query.offset(offset).limit(limite)
        ).all()

    return templates.TemplateResponse(
        request,
        "lista.html",
        {
            "alunos": alunos,
            "page": page,
            "tem_proxima": len(total) > offset + limite,
            "busca": busca
        },
    )

@app.get("/editarAlunos")
def novoAluno(request: Request):
    return templates.TemplateResponse(request, "options.html", {})

@app.post("/novoAluno", response_class=HTMLResponse)
def criar_aluno(nome: str = Form(...)):
    with Session(engine) as session:
        novo_aluno = Aluno(nome=nome)
        session.add(novo_aluno)
        session.commit()
        session.refresh(novo_aluno)
        return HTMLResponse(content=f"<p>O(a) aluno(a) {novo_aluno.nome} foi registrado(a)!</p>")

@app.delete("/deletaAluno", response_class=HTMLResponse)
def deletar_aluno(id: int):
    with Session(engine) as session:
        query = select(Aluno).where(Aluno.id == id)
        aluno = session.exec(query).first()
        if (not aluno):
            raise HTTPException(404, "Aluno não encontrado")
        session.delete(aluno)
        session.commit()
        return HTMLResponse(content=f"<p>O(a) aluno(a) {aluno.nome} foi deletado(a)!</p>")

@app.put("/atualizaAluno", response_class=HTMLResponse)
def atualizar_aluno(id: int = Form(...), novoNome: str = Form(...)):
    with Session(engine) as session:
        query = select(Aluno).where(Aluno.id == id)
        aluno = session.exec(query).first()
        if (not aluno):
            raise HTTPException(404, "Aluno não encontrado")
        nomeAntigo = aluno.nome
        aluno.nome = novoNome
        session.commit()
        session.refresh(aluno)
        return HTMLResponse(content=f"<p>O(a) aluno(a) {nomeAntigo} foi atualizado(a) para {aluno.nome}!</p>")

def buscar_alunos(busca: str = ''):
    with Session(engine) as session:
        query = select(Aluno)

        if busca:
            query = query.where(Aluno.nome.contains(busca))

        return session.exec(query).all()
    
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.delete("/apagar", response_class=HTMLResponse)
def apagar():
    return ""
