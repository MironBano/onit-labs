import os

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="LR4 node")


@app.get("/", response_class=HTMLResponse)
def index():
    node = os.environ.get("NODE_ID", "?")
    return f"""<!DOCTYPE html>
<html lang="ru"><head><meta charset="utf-8"/><title>Нода {node}</title></head>
<body><h1>Нода {node}</h1><p>ОНИТ — ЛР4 (балансировка Nginx)</p></body></html>"""


@app.get("/health")
def health():
    return {"status": "ok", "node": os.environ.get("NODE_ID", "?")}
