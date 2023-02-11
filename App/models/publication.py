from App.database import db
from sqlalchemy import ForeignKey

class Publication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    abstract = db.Column(db.String(500), nullable=False)
    free_access = db.Column(db.Boolean, nullable=False)
    pub_type = db.Column(db.String(30), nullable=False)
    pub_records = db.relationship("PubRecord", backref="publication", lazy=True, cascade="all, delete-orphan")
    lib_records = db.relationship("LibraryRecord", backref="publication", lazy=True, cascade="all, delete-orphan")

    def __init__(self, title, abstract, free_access, pub_type):
        self.title = title
        self.abstract = abstract
        self.free_access = free_access
        self.pub_type = pub_type

    def toDict(self):
        return {
            'id': self.id,
            'title': self.title,
            'abstract': self.abstract,
            'pub_type':self.pub_type,
            'free_access': self.free_access,
        }
