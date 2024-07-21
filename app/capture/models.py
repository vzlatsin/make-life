# app/capture/models.py
from app import db

class CaptureEntry(db.Model):
    __tablename__ = 'capture_entries'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<CaptureEntry {self.id}>'
