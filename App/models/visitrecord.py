from App.database import db
from sqlalchemy import ForeignKey
from datetime import datetime

class VisitRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)
    researcher_id = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)
    last_visited = db.Column(db.Date, default=datetime.today())

    def __init__(self, user_id, researcher_id):
        self.user_id = user_id
        self.researcher_id = researcher_id

    def get_todays_date(self):
        return datetime.date(datetime.today())

    def update_last_visited(self):
        self.last_visited = self.get_todays_date()