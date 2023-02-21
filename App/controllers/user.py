from App.models import Researcher, User
from App.database import db
from sqlalchemy.exc import IntegrityError

def get_user(id):
    return User.query.get(id)

def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    
    for user in users:
        print(user)
    users = [user.toDict() for user in users]
    return users


# For building Users - Builder DP
def build_user(user):
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return None
    return user
    
