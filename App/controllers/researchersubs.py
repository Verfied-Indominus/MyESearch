from App.models import ResearcherSubRecord
from App.database import db
from . import researcher, user

def create_sub(re_id, uid):
    try:
        re = researcher.get_researcher(re_id)
        sub = user.get_user(uid)
        if re == None or uid == None:
            return False
        new_re_sub = ResearcherSubRecord(user_id, researcher_id)
        db.session.add(new_re_sub)
        db.session.commit()
        return True
    except:
        return False
        

def remove_sub(sub_id):
    try:
        query = ResearcherSubRecord.query.filter_by(id=sub_id).first()
        db.session.delete(query)
        db.session.commit()
        return True
    except:
        return False

def get_subs(re_id):
    try:
        query = ResearcherSubRecord.query.filter_by(researcher_id=re_id).all()
        return query
    except:
        return None

def remove_sub(re_id,uid):
    try:
        query = ResearcherSubRecord.query.filter_by(researcher_id=re_id,user_id=uid).first()
        db.session.delete(query)
        db.session.commit()
        return True
    except:
        return False
