from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from ssh_connect import run_playbook

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/run/{playbook_id}", response_class=HTMLResponse)
async def run(playbook_id: str, request: Request):
    results = run_playbook(playbook_id)
    return templates.TemplateResponse("results.html", {
        "request": request,
        "playbook_id": playbook_id,
        "results": results
    })
