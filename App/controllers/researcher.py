from App.controllers.researchersubs import create_sub, remove_sub
from App.controllers.topic import get_topic_by_name
from App.database import db
from App.models import Researcher 
from App.models import ResearcherTag

def get_all_researchers():
    return Researcher.query.all()

def get_all_researchers_verified():
    return Researcher.query.filter_by(verified=True).all()

def add_interests_to_researcher(topics, re_id):
    for topic in topics:
        top = get_topic_by_name(topic)
        tag = ResearcherTag(re_id, top.id)
        db.session.add(tag)
    db.session.commit()
    return True

def delete_researcher_tags(re):
    for tag in re.research_interests:
        db.session.delete(tag)
        db.session.commit()
    return True

def get_researcher(id):
    return Researcher.query.get(id)

def get_researcher_by_email(email):
    return Researcher.query.filter_by(email=email).first()

def reSubscribe(sub_id, re_id):
    return create_sub(sub_id, re_id)

def reUnsubscribe(sub_id, re_id):
    return remove_sub(sub_id, re_id)

def get_subscribed_researchers(user):
    researchers = []
    for rec in user.researcher_sub_records:
        researchers.append(rec.subject)
    return researchers

def set_verified(re):
    re.verify()
    db.session.commit()

def delete_researcher(id):
    researcher = get_researcher(id)
    if not researcher:
        return False
    db.session.delete(researcher)
    db.session.commit()
    return True

def add_view(researcher):
    researcher.views += 1
    db.session.commit()

def add_search(researcher):
    researcher.searches += 1
    db.session.commit()
