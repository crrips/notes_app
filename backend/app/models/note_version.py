from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database import Base

class NoteVersion(Base):
    __tablename__ = "note_versions"

    id = Column(Integer, primary_key=True, index=True)
    note_id = Column(Integer, ForeignKey("notes.id", ondelete="CASCADE"))
    name = Column(String(100), nullable=False)
    description = Column(String(2048), nullable=False)
    created_at = Column(DateTime, default=datetime.now())

    note = relationship("Note", back_populates="versions")
    