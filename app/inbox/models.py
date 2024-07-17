# app/inbox/models.py
from app import db

class InboxEntry(db.Model):
    __tablename__ = 'inbox_entries'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<InboxEntry {self.id}>'