from App.models import TopicSubRecord
from . import user, topic

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


def delete_sub():
    pass

def delete_sub():
    pass