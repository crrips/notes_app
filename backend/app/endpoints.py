from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.note_version import NoteVersion
from services.summarizer import summarize
from services.analytics import analyze
from schemas.note import NoteSchema
from models.note import Note
from database import get_db

router = APIRouter()

@router.get("/notes")
def get_all_notes(db: Session = Depends(get_db)):
    notes = db.query(Note).all()
    return notes

@router.post("/notes")
def create_note(note: NoteSchema, db: Session = Depends(get_db)):
    new_note = Note(name=note.name, description=note.description)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@router.get("/notes/{id}")
def get_note_by_id(id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.put("/notes/{id}")
def update_note(note: NoteSchema, db: Session = Depends(get_db)):
    edited_note = db.query(Note).filter(Note.id == note.id).first()
    
    if not edited_note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    note_version = NoteVersion(note_id=edited_note.id, name=edited_note.name, description=edited_note.description)
    db.add(note_version)
    
    edited_note.name = note.name
    edited_note.description = note.description
    edited_note.updated_at = datetime.now()
    db.commit()
    db.refresh(edited_note)
    return edited_note

@router.delete("/notes/{id}")
def delete_note(id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    name = note.name
    db.delete(note)
    db.commit()
    return {"message": f"Note {name} has been deleted successfully"}

@router.post("/notes/summarize/{id}")
def summarize_note_by_id(id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == id).first()
    
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    summary = summarize(note.description)
    return summary

@router.get("/analytics")
def get_analytics(db: Session = Depends(get_db)):
    notes = db.query(Note).all()
    if not notes:
        return {"message": "No notes found"}
    analytics = analyze(notes)
    return analytics

def get_router() -> APIRouter:
    return router
