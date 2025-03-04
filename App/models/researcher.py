from App.models import User
from App.database import db
from flask_login import UserMixin

class Researcher(UserMixin, User):
    title = db.Column(db.String(8))
    position = db.Column(db.String(100))
    start_year = db.Column(db.String(8))
    qualifications = db.Column(db.String(300))
    certifications = db.Column(db.String(300))
    skills = db.Column(db.String(300))
    website_url = db.Column(db.String(120))
    introduction = db.Column(db.String(500))
    views = db.Column(db.Integer)
    searches = db.Column(db.Integer)
    verified = db.Column(db.Boolean)
    research_interests = db.relationship("ResearcherTag", backref="researcher", lazy="dynamic", cascade="all, delete-orphan")
    pub_records = db.relationship("PubRecord", backref="researcher", lazy="dynamic", cascade="all, delete-orphan")
    sub_records = db.relationship("ResearcherSubRecord", foreign_keys='ResearcherSubRecord.researcher_id', backref="subject", lazy="dynamic", cascade="all, delete-orphan")

    __mapper_args__ = {
        'polymorphic_identity':'Researcher'
    }

    def __init__(self):
        super(Researcher, self).__init__()
        self.views = 0
        self.searches = 0
        self.verified = False

    def verify(self):
        self.verified = True

    def toDict(self):
        return super().toDict() | {
            'title': self.title,
            'position': self.position,
            'start_year': self.start_year,
            'qualifications': self.qualifications,
            'certifications': self.certifications,
            'skills': self.skills,
            'website_url': self.website_url,
            'introduction': self.introduction,
            'subs': [rec.toDict() for rec in self.sub_records.all()]
        }

    def toDictPub(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'image_url': self.image_url
        }
