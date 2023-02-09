from App.database import db
from sqlalchemy import ForeignKey, TIMESTAMP
from sqlalchemy.sql import func

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False)
    message = db.Column(db.String(120), nullable=False)
    timestamp = db.Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=db.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    notification_records = db.relationship("NotificationRecord", backref="notification", lazy=True, cascade="all, delete-orphan")

    def __init__(self, title, message):
        self.title = title
        self.message = message