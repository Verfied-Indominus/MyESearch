from App.controllers.notification import notify_subscribers_author
from App.database import db
from App.models.pubrecord import PubRecord

def add_pub_record(re_id, pub_id):
    # pubrec = get_pub_record(re_id, pub_id)
    # if not pubrec:
    pubrec = PubRecord(re_id, pub_id)
    db.session.add(pubrec)
    db.session.commit()
    notify_subscribers_author(re_id, pub_id)
    return True
    # return False

def delete_pub_record(re_id, pub_id):
    pubrec = get_pub_record(re_id, pub_id)
    if pubrec:
        db.session.delete(pubrec)
        db.session.commit()
        return True
    return False

def get_pub_record(re_id, pub_id):
    return PubRecord.query.filter_by(researcher_id=re_id, publication_id=pub_id).first()