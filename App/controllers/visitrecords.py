from App.database import db
from App.models.visitrecord import VisitRecord
from sqlalchemy.exc import IntegrityError

def create_visit_record(user_id, re_id):
    vrec = VisitRecord(user_id, re_id)
    try:
        db.session.add(vrec)
        db.session.commit()
        return vrec
    except IntegrityError:
        db.session.rollback()
        return None

def get_visit_record(user_id, re_id):
    return VisitRecord.query.filter_by(user_id=user_id, researcher_id=re_id).first()

def update_visit_record(vrec):
    if vrec.get_todays_date() > vrec.last_visited:
        vrec.update_last_visited()
        db.session.add(vrec)
        db.session.commit()
        return True
    return False
