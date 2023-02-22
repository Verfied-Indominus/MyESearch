from App.models import Student
from App.database import db

def query_by_id(id):
    query = Student.query.filter_by(id=id).first()
    if not query:
        return None
    return query

def query_student(name): #let name be a dict of first and last name
    query= Student.query.filter_by(first_name=name["first_name"])
    query = query.filter_by(last_name=name["last_name"]).first()
    if not query:
        return None
    return query
    
def delete_student(id):
    try:
        query = Student.query.filter_by(id=id).first()
        db.session.delete(query)
        db.session.commit()
        return True
    except:
        return False

