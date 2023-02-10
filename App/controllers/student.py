from App.models import student
from App.database import db


def query_by_id(id):
    query = student.query.filter_by(id=id).first()
    if not query:
        return None
    return query

def query_student(name): #let name be a dict of first and last name
    query= student.query.filter_by(first_name=name["first_name"])
    query = query.filter_by(last_name=last_name).first()
    if not query:
        return None
    return query
    

def create_student(data): #let args be a dictionary
    try:
        new_Student = student(
            email =data["email"],
            first_name=data["first_name"],
            middle_name=data["middle_name"],
            last_name=data["last_name"],
            institution=data["institution"],
            department=data["department"],
            image_url=data["image_url"]
            )
        db.session.add(new_Student)
        db.session.commit()
        return True
    except:
        return False


def delete_student(id):
    try:
        query = student.filter_by(id=id).first()
        db.session.delete(query)
        db.session.commit()
    except:
        return False
    return True

def update_student(id,data): #let data be a dictionary of thr information
    student = query_by_id(id)
    if not student:
        return False
    student.image_url = data["image_url"]
    student.institution = data["institution"]
    student.email = data["email"]
    db.session.commit()
    return True
    