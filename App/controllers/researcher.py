from App.database import db
from App.models import Researcher 

def get_researcher(id):
    return Researcher.query.get(id)

def get_researcher_by_email(email):
    return Researcher.query.filter_by(email=email).first()

def get_subscribed_researchers(user):
    researchers = []
    for rec in user.researcher_sub_records:
        researchers.append(rec.researcher)
    return researchers

def delete_researcher(id):
    researcher = get_researcher(id)
    if not researcher:
        return False
    db.session.delete(researcher)
    db.session.commit()
    return True

def add_view(researcher):
    researcher.views += 1
    db.session.add(researcher)
    db.session.commit()
    return researcher

def add_search(researcher):
    researcher.searches += 1
    db.session.add(researcher)
    db.session.commit()
    return researcher
