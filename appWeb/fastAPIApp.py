from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def accueil(request: Request):
    return templates.TemplateResponse(
        request=request, name="accueilVoc.html"
    )

@app.get("/Request",response_class=HTMLResponse)
async def reponse(request: Request,text):
    return templates.TemplateResponse(
        request=request
    )