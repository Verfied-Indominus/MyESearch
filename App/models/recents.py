from App.database import db
from sqlalchemy import ForeignKey

class Recents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)
    records = db.relationship("RecentsRecord", backref="recents", lazy=True, cascade="all, delete-orphan")

    def __init__(self, user_id):
        self.user_id = user_id

    def toDict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'records': self.records
        }