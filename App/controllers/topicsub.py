from App.models import TopicSubRecord
from . import user, topic,notification,publication
from App.database import db

def create_sub(tid,uid):
    try:
        use = user.get_user(uid)
        top = topic.get_topic_id(tid)
        if top is None or use is None:
            return False
        new_top_sub = TopicSubRecord(uid, tid)
        db.session.add(new_top_sub)
        db.session.commit()
        return True
    except:
        return False
    

def get_subs(tid):
    return TopicSubRecord.query.filter_by(id=tid).all()

def delete_sub_id(sid):
    try:
        sub = TopicSubRecord.query.filter_by(id=sid).first()
        if sub is None:
            return False
        db.session.delete(sub)
        db.session.commit()
    except:
        return False
        
def delete_sub(tid,uid):
    try:
        use = user.get_user(uid)
        top = topic.get_topic_id(tid)
        if top is None or use is None:
            return False
        sub  = TopicSubRecord.query.filter_by(user_id = uid,topic_id=tid).first()
        db.session.delete(sub)
        db.session.commit()
        return True
    except:
        return False
    
def topic_notification(tid,pid):
    try:
        top = topic.get_topic_id(tid)
        pub = publication.get_pub_byid(pid)
        subs = TopicSubRecord.query.filter_by(topic_id=tid).all()
        title = f"New publication under {top.name}"
        message = f"New publication addded: {pub.title}"
        notification.notify_subscribers(subs,title,message)
        return True
    except:
        return False