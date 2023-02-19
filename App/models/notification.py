from App.database import db
from sqlalchemy import ForeignKey, TIMESTAMP
from sqlalchemy.sql import func


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False)
    message = db.Column(db.String(120), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, server_default=func.now())
    last_updated = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    notification_records = db.relationship("NotificationRecord", backref="notification", lazy=True, cascade="all, delete-orphan")

    def __init__(self, title, message):
        self.title = title
        self.message = message
    
    def toDict(self):
        return {
            'id': self.id,
            'title': self.title,
            'message': self.message,
            'timestamp': self.timestamp,
            'last_updated': self.last_updated,
            'notification_records': self.notification_records
        }