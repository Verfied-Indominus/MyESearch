from App.models import Student
from App.database import db


def query_by_id(id):
    query = Student.query.filter_by(id=id).first()
    if not query:
        return None
    return query

def query_student(name): #let name be a dict of first and last name
    query= Student.query.filter_by(first_name=name["first_name"])
    query = query.filter_by(last_name=last_name).first()
    if not query:
        return None
    return query
    

def create_student(data): #let args be a dictionary
    try:
        new_Student = Student(
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
        query = Student.filter_by(id=id).first()
        db.session.delete(query)
        db.session.commit()
        return True
    except:
        return False
   

def update_student(id,data): #let data be a dictionary of thr information
    Student = query_by_id(id)
    if not Student:
        return False
    Student.image_url = data["image_url"]
    Student.institution = data["institution"]
    Student.email = data["email"]
    db.session.commit()
    return True
    