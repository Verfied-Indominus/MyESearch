from App.models import Researcher, User
from App.database import db
from sqlalchemy.exc import IntegrityError

def get_user(id):
    return User.query.get(id)

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


# # User Builder controllers

# def new_student():
#     return Student()

# def user_first_name(user, first_name):
#     user.first_name = first_name
#     return user

# def user_middle_name(user, middle_name):
#     user.middle_name = middle_name
#     return user

# def user_last_name(user, last_name):
#     user.last_name = last_name
#     return user

# def user_email(user, email):
#     user.email = email
#     return user

# def user_password(user, password):
#     user.password = password
#     return user 

# def user_image_url(user, image_url):
#     user.image_url = image_url
#     return user

# def user_affiliation(user, institution, faculty, department):
#     user.institution = institution
#     user.faculty = faculty
#     user.department = department
#     return user

# def user_title(user, title):
#     user.title = title
#     return user

# def user_position(user, position):
#     user.position = position
#     return user

# def user_start_year(user, year):
#     user.start_year = year
#     return user

# def user_qualifications(user, qualifications):
#     user.qualifications = qualifications
#     return user

# def user_certifications(user, certifications):
#     user.certifications = certifications
#     return user



def build_user(user):
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        print('WRONG')
        return None
    return user
    
