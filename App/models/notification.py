from sqlalchemy.sql import func
from App.database import db



class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    message = db.Column(db.String(1000), nullable=True)
    type = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, server_default=func.now())
    last_updated = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    notification_records = db.relationship("NotificationRecord", backref="notification", lazy="dynamic", cascade="all, delete-orphan")

    def __init__(self, title, message, type):
        self.title = title
        self.message = message
        self.type = type
    
    def toDict(self):
        return {
            'id': self.id,
            'title': self.title,
            'message': self.message,
            'timestamp': self.timestamp,
            'last_updated': self.last_updated,
            'notification_records': self.notification_records.all()
        }