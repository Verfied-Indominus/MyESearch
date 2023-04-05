from App.database import db
from sqlalchemy import ForeignKey

class RecentsRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recents_id = db.Column(db.Integer, ForeignKey("recents.id"), nullable=False)
    publication_id = db.Column(db.Integer, ForeignKey("publication.id"), nullable=False)

    def __init__(self, recents_id, publication_id):
        self.recents_id = recents_id
        self.publication_id = publication_id