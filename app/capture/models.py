from app import db
from datetime import datetime, timezone

class CaptureEntry(db.Model):
    __tablename__ = 'capture_entries'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    handled = db.Column(db.Boolean, default=False)
    organized = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    processed_at = db.Column(db.DateTime)

    def __repr__(self):
        return f'<CaptureEntry {self.id}>'
