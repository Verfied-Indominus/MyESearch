from App.database import db
from sqlalchemy import ForeignKey

class Publication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    abstract = db.Column(db.String(500), nullable=False)
    free_access = db.Column(db.Boolean, nullable=False)
    pub_type = db.Column(db.String(30), nullable=False)
    publication_date = db.Column(db.DateTime, nullable=False)
    tags = db.ralationship("PublicationTag", backref="publication", lazy="dynamic", cascade="all, delete-orphan")
    pub_records = db.relationship("PubRecord", backref="publication", lazy="dynamic", cascade="all, delete-orphan")
    lib_records = db.relationship("LibraryRecord", backref="publication", lazy="dynamic", cascade="all, delete-orphan")

    def __init__(self, title, abstract, free_access, pub_type, publication_date):
        self.title = title
        self.abstract = abstract
        self.free_access = free_access
        self.pub_type = pub_type
        self.publication_date = publication_date

    def toDict(self):
        return {
            'id': self.id,
            'title': self.title,
            'abstract': self.abstract,
            'pub_type':self.pub_type,
            'free_access': self.free_access,
            'publicatiion_date': self.publication_date
        }
