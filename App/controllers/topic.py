from App.database import db
from App.models import Topic
from sqlalchemy.exc import IntegrityError

def create_topic(name):
    topic = Topic(name)
    try:
        db.session.add(topic)
        db.session.commit()
    except IntegrityError:
        return None
    return topic

def get_topic(id):
    return Topic.query.filter_by(id=id).first()

def get_topic_by_name(name):
    return Topic.query.filter_by(name=name).first()

def get_topic_id(id):
    return Topic.query.filter_by(id=id).first()

def get_all_topics():
    return [topic.toDict() for topic in Topic.query.all()]

def get_topics(limiter):
    return [topic.toDict() for topic in Topic.query.limit(limiter)]

def set_topic_parent(name, id):
    try:
        topic = get_topic_by_name(name)
        topic.set_parent_id(id)
        db.session.add(topic)
        db.session.commit()
        return topic
    except:
        return None

def delete_topic(name):
    try:
        topic = get_topic_by_name(name)
        db.session.delete(topic)
        db.session.commit()
        return True
    except:
        return False
