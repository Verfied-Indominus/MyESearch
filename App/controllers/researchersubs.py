from App.models import ResearcherSubRecord
from App.database import db
from . import researcher, user

def create_sub(uid, re_id):
    try:
        re = researcher.get_researcher(re_id)
        sub = user.get_user(uid)
        if re is None or uid is None:
            return False
        sub = ResearcherSubRecord.query.filter_by(user_id=uid, researcher_id=re_id).first()
        if sub:
            return False;
        new_re_sub = ResearcherSubRecord(uid, re_id)
        db.session.add(new_re_sub)
        db.session.commit()
        return True
    except:
        return False
        

def remove_sub_id(sub_id):
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

def remove_sub(uid, re_id):
    try:
        query = ResearcherSubRecord.query.filter_by(researcher_id=re_id,user_id=uid).first()
        db.session.delete(query)
        db.session.commit()
        return True
    except:
        return False

# def researcher_notification(re_id,pid):
#     try:
#         re = researcher.get_researcher(re_id)
#         subs = get_subs(re_id)
#         pub = publication.get_pub_byid(pid)
#         title = f"New publication from: {re.first_name} {re.last_name}"
#         message = f"New publication added: {pub.title}"
#         notification.notify_subscribers(re,title,message)
#         return True
#     except:
#         return False