from App.database import db

class Publication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    abstract = db.Column(db.String(2000), nullable=False)
    free_access = db.Column(db.Boolean, nullable=False)
    pub_type = db.Column(db.String(30), nullable=False)
    publication_date = db.Column(db.Date, nullable=False)
    reads = db.Column(db.Integer, nullable=False)
    citations = db.Column(db.Integer, nullable=False)
    downloads = db.Column(db.Integer, nullable=False)
    searches = db.Column(db.Integer, nullable=False)
    cover = db.Column(db.String(120))
    url = db.Column(db.String(120))
    eprint = db.Column(db.String(120))
    coauthors = db.Column(db.String(100))
    tags = db.relationship("PublicationTag", backref="publication", lazy="dynamic", cascade="all, delete-orphan")
    pub_records = db.relationship("PubRecord", backref="publication", lazy="dynamic", cascade="all, delete-orphan")
    lib_records = db.relationship("LibraryRecord", backref="publication", lazy="dynamic", cascade="all, delete-orphan")

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
            'publication_date': self.publication_date,
            'cover': self.cover,
            'url': self.url,
            'eprint': self.eprint,
            'reads': self.reads,
            'citations': self.citations,
            'downloads': self.downloads,
            'searches': self.searches
        }
