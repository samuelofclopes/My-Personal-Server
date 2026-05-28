from extensions import db
from datetime import datetime, timezone


class Message(db.Model):
    __tablename__ = 'messages'
    id =           db.Column(db.Integer, primary_key=True)
    content =      db.Column(db.String(400), nullable=False)
    user =         db.Column(db.String(20),nullable=False)
    created_at =      db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))