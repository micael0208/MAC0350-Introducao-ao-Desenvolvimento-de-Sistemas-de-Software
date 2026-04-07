# Arquivo main.py

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from models import Caso, Evidencia
from contextlib import asynccontextmanager
from sqlmodel import SQLModel, create_engine, Session, select
from sqlalchemy.orm import selectinload
from datetime import datetime

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

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {})

@app.post("/casos", response_class=HTMLResponse)
def criar_caso(
    request: Request,
    titulo: str = Form(...),
    descricao: str = Form(...),
    status: str = Form(...),
    classificacao: str = Form(...),
    prioridade: str = Form(...)
):
    with Session(engine) as session:
        caso = Caso(
            titulo=titulo,
            descricao=descricao,
            status=status,
            classificacao=classificacao,
            prioridade=prioridade
        )
        session.add(caso)
        session.commit()
        session.refresh(caso)

    return templates.TemplateResponse(
        request,
        "partials/caso_item.html",
        {"caso": caso}
    )

@app.delete("/casos/{caso_id}")
def deletar_caso(caso_id: int):
    with Session(engine) as session:
        caso = session.get(Caso, caso_id)
        if not caso:
            raise HTTPException(404, "Caso não encontrado")

        session.delete(caso)
        session.commit()

    return ""

@app.put("/casos/{caso_id}")
def atualizar_status(caso_id: int, status: str = Form(...)):
    with Session(engine) as session:
        caso = session.get(Caso, caso_id)
        if not caso:
            raise HTTPException(404, "Caso não encontrado")

        caso.status = status
        session.commit()
        session.refresh(caso)

    return templates.TemplateResponse(
        "partials/caso_item.html",
        {"caso": caso}
    )

@app.post("/evidencias")
def criar_evidencia(
    request: Request,
    descricao: str = Form(...),
    categoria: str = Form(...),
    status_atual: str = Form(...),
    coletado_onde: str = Form(None),
    caso_id: int = Form(...)
):
    with Session(engine) as session:
        evidencia = Evidencia(
            descricao=descricao,
            categoria=categoria,
            status_atual=status_atual,
            coletado_onde=coletado_onde,
            coletado_quando=datetime.utcnow(),
            caso_id=caso_id
        )
        session.add(evidencia)
        session.commit()
        session.refresh(evidencia)

        caso = session.exec(
            select(Caso)
            .where(Caso.id == caso_id)
            .options(selectinload(Caso.evidencias))
        ).first()

    return templates.TemplateResponse(
        request,
        "partials/evidencias_lista.html",
        {"caso": caso}
    )

@app.get("/casos/{caso_id}/evidencias", response_class=HTMLResponse)
def listar_evidencias(request: Request, caso_id: int):
    with Session(engine) as session:
        caso = session.exec(
            select(Caso)
            .where(Caso.id == caso_id)
            .options(selectinload(Caso.evidencias))
        ).first()

    return templates.TemplateResponse(
        request,
        "partials/evidencias_lista.html",
        {"caso": caso}
    )

@app.get("/casos", response_class=HTMLResponse)
def listar_casos(
    request: Request,
    busca: str = "",
    classificacao: str = "",
    status: str = "",
    prioridade: str = "",
    page: int = 1
):
    limite = 5
    offset = (page - 1) * limite

    with Session(engine) as session:
        query = select(Caso)

        if busca:
            query = query.where(Caso.titulo.contains(busca))

        if classificacao:
            query = query.where(Caso.classificacao == classificacao)

        if status:
            query = query.where(Caso.status == status)

        if prioridade:
            query = query.where(Caso.prioridade == prioridade)

        total = session.exec(query).all()

        casos = session.exec(
            query.offset(offset).limit(limite)
        ).all()

    context = {
        "casos": casos,
        "busca": busca,
        "classificacao": classificacao,
        "status": status,
        "prioridade": prioridade,
        "page": page,
        "tem_proxima": len(total) > offset + limite
    }

    if request.headers.get("HX-Request"):
        return templates.TemplateResponse(
            request,
            "partials/casos_lista.html",
            context
        )

    return templates.TemplateResponse(
        request,
        "casos.html",
        context
    )

@app.get("/casos/{caso_id}/editar")
def editar_caso_form(request: Request, caso_id: int):
    with Session(engine) as session:
        caso = session.get(Caso, caso_id)

    return templates.TemplateResponse(
        request,
        "partials/caso_edit.html",
        {"caso": caso}
    )

@app.put("/casos/{caso_id}/editar")
def atualizar_descricao(
    request: Request,
    caso_id: int,
    descricao: str = Form(...)
):
    with Session(engine) as session:
        caso = session.get(Caso, caso_id)
        caso.descricao = descricao
        session.commit()
        session.refresh(caso)

    return templates.TemplateResponse(
        request,
        "partials/caso_item.html",
        {"caso": caso}
    )

@app.get("/evidencias/{evidencia_id}/editar")
def editar_evidencia_form(request: Request, evidencia_id: int):
    with Session(engine) as session:
        evidencia = session.get(Evidencia, evidencia_id)

    return templates.TemplateResponse(
        request,
        "partials/evidencia_edit.html",
        {"evidencia": evidencia}
    )

@app.put("/evidencias/{evidencia_id}")
def atualizar_evidencia(
    request: Request,
    evidencia_id: int,
    descricao: str = Form(...),
    status_atual: str = Form(...)
):
    with Session(engine) as session:
        evidencia = session.get(Evidencia, evidencia_id)
        evidencia.descricao = descricao
        evidencia.status_atual = status_atual

        session.commit()
        session.refresh(evidencia)

    return templates.TemplateResponse(
        request,
        "partials/evidencia_item.html",
        {"evidencia": evidencia}
    )

@app.delete("/evidencias/{evidencia_id}")
def deletar_evidencia(request: Request, evidencia_id: int):
    with Session(engine) as session:
        evidencia = session.get(Evidencia, evidencia_id)

        if not evidencia:
            raise HTTPException(404, "Evidência não encontrada")

        caso_id = evidencia.caso_id 

        session.delete(evidencia)
        session.commit()

        caso = session.exec(
            select(Caso)
            .where(Caso.id == caso_id)
            .options(selectinload(Caso.evidencias))
        ).first()

    return templates.TemplateResponse(
        request,
        "partials/evidencias_lista.html",
        {"caso": caso}
    )

app.mount("/static", StaticFiles(directory="static"), name="static")