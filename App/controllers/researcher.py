from App.database import db
from App.models import Researcher 
from App.models import ResearcherTag
from App.models import PubRecord
from App.controllers import get_topic_by_name

def get_all_researchers():
    return Researcher.query.all()

def add_publication_to_researcher(re_id, pub_id):
    try:
        record = PubRecord(re_id, pub_id)
        db.session.add(record)
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        return False
    
def add_interests_to_researcher(interests, re_id):
    for int in interests:
        topic = get_topic_by_name(int)
        if not topic:
            return False
        tag = ResearcherTag(re_id, topic.id)
        db.session.add(tag)
    db.session.commit()
    return True

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
