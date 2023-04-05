from App.database import db
import datetime
from datetime import datetime

class Publication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    abstract = db.Column(db.String(2000), nullable=False)
    free_access = db.Column(db.Boolean, nullable=False)
    pub_type = db.Column(db.String(30), nullable=False)
    publication_date = db.Column(db.Date, nullable=False)
    url = db.Column(db.String(400))
    eprint = db.Column(db.String(400))
    coauthors = db.Column(db.String(425))
    bibtex = db.Column(db.String(1000))
    reads = db.Column(db.Integer, nullable=False)
    citations = db.Column(db.Integer, nullable=False)
    downloads = db.Column(db.Integer, nullable=False)
    searches = db.Column(db.Integer, nullable=False)
    encryptedPDF = db.Column(db.String(200))
    tags = db.relationship("PublicationTag", backref="publication", lazy="dynamic", cascade="all, delete-orphan")
    pub_records = db.relationship("PubRecord", backref="publication", lazy="joined", innerjoin=True, cascade="all, delete-orphan")
    lib_records = db.relationship("LibraryRecord", backref="lib_pub", lazy="dynamic", cascade="all, delete-orphan")
    recents_records = db.relationship("RecentsRecord", backref="recents_pub", lazy="dynamic", cascade="all, delete-orphan")

    def __init__(self, title, abstract, free_access, pub_type, publication_date, url, eprint):
        self.title = title
        self.abstract = abstract
        self.free_access = free_access
        self.pub_type = pub_type
        self.publication_date = publication_date
        self.url = url
        self.eprint = eprint
        self.reads = 0
        self.citations = 0
        self.downloads = 0
        self.searches = 0

    def add_coauthors_string(self, coauthors):
        self.coauthors = coauthors

    def toDict(self):
        return {
            'id': self.id,
            'title': self.title,
            'abstract': self.abstract,
            'pub_type':self.pub_type,
            'free_access': self.free_access,
            'publication_date': datetime.strftime(self.publication_date, '%Y'),
            'url': self.url,
            'eprint': self.eprint,
            'coauthors': self.coauthors,
            'reads': self.reads,
            'citations': self.citations,
            'downloads': self.downloads,
            'searches': self.searches,
            'coauthors': self.coauthors,
            'authors': [rec.researcher.toDictPub() for rec in self.pub_records]
        }
    
    def toDictQuick(self):
        return {
            'id': self.id,
            'title': self.title,
            'abstract': self.abstract,
            'pub_type':self.pub_type,
            'free_access': self.free_access,
            'publication_date': datetime.strftime(self.publication_date, '%Y'),
            'url': self.url,
            'eprint': self.eprint,
            'coauthors': self.coauthors,
            'reads': self.reads,
            'citations': self.citations,
            'downloads': self.downloads,
            'searches': self.searches,
            'coauthors': self.coauthors,
            # 'authors': [rec.researcher.toDictPub() for rec in self.pub_records]
        }
