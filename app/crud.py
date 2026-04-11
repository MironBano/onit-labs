from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models


def list_notes(db: Session):
    stmt = select(models.Note).order_by(models.Note.id.desc())
    return list(db.scalars(stmt))


def get_note(db: Session, note_id: int) -> models.Note | None:
    return db.get(models.Note, note_id)


def create_note(db: Session, title: str, body: str) -> models.Note:
    note = models.Note(title=title, body=body or "")
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def update_note(db: Session, note_id: int, title: str, body: str) -> models.Note | None:
    note = get_note(db, note_id)
    if note is None:
        return None
    note.title = title
    note.body = body or ""
    db.commit()
    db.refresh(note)
    return note


def delete_note(db: Session, note_id: int) -> bool:
    note = get_note(db, note_id)
    if note is None:
        return False
    db.delete(note)
    db.commit()
    return True
