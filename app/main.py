from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app import crud
from app.database import Base, get_db, init_engine

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_engine()
    from app.database import engine

    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Заметки (ОНИТ ЛР1–2)", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    notes = crud.list_notes(db)
    return templates.TemplateResponse(
        request,
        "list.html",
        {"notes": notes},
    )


@app.get("/notes/new", response_class=HTMLResponse)
def new_form(request: Request):
    return templates.TemplateResponse(
        request,
        "form.html",
        {"note": None, "action": "create"},
    )


@app.post("/notes/new")
def create(
    title: str = Form(...),
    body: str = Form(""),
    db: Session = Depends(get_db),
):
    crud.create_note(db, title.strip(), body)
    return RedirectResponse("/", status_code=303)


@app.get("/notes/{note_id}/edit", response_class=HTMLResponse)
def edit_form(note_id: int, request: Request, db: Session = Depends(get_db)):
    note = crud.get_note(db, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Заметка не найдена")
    return templates.TemplateResponse(
        request,
        "form.html",
        {"note": note, "action": "edit"},
    )


@app.post("/notes/{note_id}/edit")
def update(
    note_id: int,
    title: str = Form(...),
    body: str = Form(""),
    db: Session = Depends(get_db),
):
    note = crud.update_note(db, note_id, title.strip(), body)
    if note is None:
        raise HTTPException(status_code=404, detail="Заметка не найдена")
    return RedirectResponse("/", status_code=303)


@app.post("/notes/{note_id}/delete")
def delete(note_id: int, db: Session = Depends(get_db)):
    if not crud.delete_note(db, note_id):
        raise HTTPException(status_code=404, detail="Заметка не найдена")
    return RedirectResponse("/", status_code=303)
