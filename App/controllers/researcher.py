from App.database import db
from App.models import Researcher 


# this would change when builder design pattern is applied
def create_researcher(email, password, first_name, middle_name, last_name, institution, faculty, department, title, position, 
                    start_year, qualifications, certifications, skills, website_url, introduction):
    newresearcher = Researcher(email, password, first_name, middle_name, last_name, institution, faculty, department, title, 
                                position, start_year, qualifications, certifications, skills, website_url, introduction)
    db.session.add(newresearcher)
    db.session.commit()
    return newresearcher

def get_researcher(id):
    return Researcher.query.get(id)

def get_researcher_by_email(email):
    return Researcher.query.filter_by(email=email).first()

def update_researcher_fname(id, fname):
    researcher = get_researcher(id)
    if not researcher:
        return False
    researcher.first_name = fname
    db.session.add(researcher)
    db.session.commit()
    return True
    
def update_researcher_midname(id, midname):
    researcher = get_researcher(id)
    if not researcher:
        return False
    researcher.middle_name = midname
    db.session.add(researcher)
    db.session.commit()
    return True

def update_researcher_lname(id, lname):
    researcher = get_researcher(id)
    if not researcher:
        return False
    researcher.last_name = lname
    db.session.add(researcher)
    db.session.commit()
    return True

def update_researcher_institution(id, institution):
    researcher = get_researcher(id)
    if not researcher:
        return False
    researcher.institution = institution
    db.session.add(researcher)
    db.session.commit()
    return True

def update_researcher_faculty(id, faculty):
    researcher = get_researcher(id)
    if not researcher:
        return False
    researcher.faculty = faculty
    db.session.add(researcher)
    db.session.commit()
    return True

def update_researcher_department(id, department):
    researcher = get_researcher(id)
    if not researcher:
        return False
    researcher.department = department
    db.session.add(researcher)
    db.session.commit()
    return True

def update_researcher_title(id, title):
    researcher = get_researcher(id)
    if not researcher:
        return False
    researcher.title = title
    db.session.add(researcher)
    db.session.commit()
    return True

def update_researcher_position(id, position):
    researcher = get_researcher(id)
    if not researcher:
        return False
    researcher.position = position
    db.session.add(researcher)
    db.session.commit()
    return True

def update_researcher_start_year(id, start_year):
    researcher = get_researcher(id)
    if not researcher:
        return False
    researcher.start_year = start_year
    db.session.add(researcher)
    db.session.commit()
    return True

def update_researcher_qualifications(id, qualifications):
    researcher = get_researcher(id)
    if not researcher:
        return False
    researcher.qualifications = qualifications
    db.session.add(researcher)
    db.session.commit()
    return True

def update_researcher_certifications(id, certifications):
    researcher = get_researcher(id)
    if not researcher:
        return False
    researcher.certifications = certifications
    db.session.add(researcher)
    db.session.commit()
    return True

def update_researcher_skills(id, skills):
    researcher = get_researcher(id)
    if not researcher:
        return False
    researcher.skills = skills
    db.session.add(researcher)
    db.session.commit()
    return True

def update_researcher_website_url(id, website_url):
    researcher = get_researcher(id)
    if not researcher:
        return False
    researcher.website_url = website_url
    db.session.add(researcher)
    db.session.commit()
    return True

def update_researcher_introduction(id, introduction):
    researcher = get_researcher(id)
    if not researcher:
        return False
    researcher.introduction = introduction
    db.session.add(researcher)
    db.session.commit()
    return True

def delete_researcher(id):
    researcher = get_researcher(id)
    if not researcher:
        return False
    db.session.delete(researcher)
    db.session.commit()
    return True