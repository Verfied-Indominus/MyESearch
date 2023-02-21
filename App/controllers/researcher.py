from App.database import db
from App.models import Researcher 

def get_researcher(id):
    return Researcher.query.get(id)

def get_researcher_by_email(email):
    return Researcher.query.filter_by(email=email).first()

def delete_researcher(id):
    researcher = get_researcher(id)
    if not researcher:
        return False
    db.session.delete(researcher)
    db.session.commit()
    return True

