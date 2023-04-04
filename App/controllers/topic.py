from App.database import db
from App.models import Topic
from sqlalchemy.exc import IntegrityError
from random import shuffle

def create_topic(name):
    topic = Topic(name)
    try:
        db.session.add(topic)
        db.session.commit()
    except IntegrityError:
        return None
    return topic

def create_topic_with_parent(name, parent_id):
    topic = Topic(name)
    topic.set_parent_id(parent_id)
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
    return Topic.query.all()

def get_all_topics_json():
    return [topic.toDict() for topic in Topic.query.all()]

def get_signup_topics():
    topics = Topic.query.limit(10).all()
    temp = Topic.query.offset(10).all()
    shuffle(temp)
    topics.extend(temp[:10])
    shuffle(topics)
    return topics

def get_topics(limiter):
    return [topic.toDict() for topic in Topic.query.limit(limiter)]

def get_subscribed_topics(user):
    topics = []
    for rec in user.topic_sub_records:
        topics.append(rec.topic)
    return topics

def get_research_topics(researcher):
    topics = []
    for tag in researcher.research_interests:
        topics.append(tag.topic)
    return topics

def set_topic_parent(name, id):
    try:
        topic = get_topic_by_name(name)
        topic.set_parent_id(id)
        db.session.add(topic)
        db.session.commit()
        return topic
    except:
        return None

def update_topic(id, name):
    topic = get_topic_id(id)
    topic.name = name
    db.session.commit()
    return topic

def delete_topic(name):
    try:
        topic = get_topic_by_name(name)
        db.session.delete(topic)
        db.session.commit()
        return True
    except Exception as e:
        print(type(e))
        return False
