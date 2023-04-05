from App.controllers.user import get_user
from App.database import db
from App.models import Researcher 
from App.models import ResearcherTag

def get_all_researchers():
    return Researcher.query.all()

def add_interests_to_researcher(topics, re_id):
    for topic in topics:
        tag = ResearcherTag(re_id, topic.id)
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

# def follow_researcher(sub_id, re_id):
#     if not create_sub(sub_id, re_id):


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
    db.session.commit()

def add_search(researcher):
    researcher.searches += 1
    db.session.commit()
