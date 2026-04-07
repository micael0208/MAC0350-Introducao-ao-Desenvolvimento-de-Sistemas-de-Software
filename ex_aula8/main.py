from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

curtidas = 0


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request, "base.html", {})


@app.get("/curtidas", response_class=HTMLResponse)
def pagina_curtidas(request: Request):
    return templates.TemplateResponse(
        request,
        "curtidas.html",
        {"curtidas": curtidas}
    )


@app.post("/curtir", response_class=HTMLResponse)
def curtir():
    global curtidas
    curtidas += 1
    return str(curtidas)


@app.delete("/curtir", response_class=HTMLResponse)
def resetar():
    global curtidas
    curtidas = 0
    return str(curtidas)

@app.get("/jupiter", response_class=HTMLResponse)
def jupiter(request: Request):
    return templates.TemplateResponse(request, "jupiter.html", {})


@app.get("/professor", response_class=HTMLResponse)
def professor(request: Request):
    return templates.TemplateResponse(request, "professor.html", {})
