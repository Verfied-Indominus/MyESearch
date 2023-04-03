from App.models import Researcher
from .scholarly_py import verify_author
from .email_py import sendEmail
from .notification import verify_author_notif
from App.database import db
from flask import request
import random

def verify_process(auth_id):
    auth = Researcher.query.filter_by(id = auth_id).first()
    department_auths = Researcher.query.filter_by(department = auth.department).all()
    faculty_auths = Researcher.query.filter_by(faculty = auth.faculty).all()
    is_auth = verify_author(f"{auth.first_name} {auth.last_name}")
    title = "Author Verification"

    if is_auth :
        auth.verify()
        db.session.commit()
        return True
    
    if department_auths != []:
        verifier = random.choice(department_auths)
        ver = f"/verify/{verifier.id}/{auth_id}"
        message = f"""
        Hi {verifier.first_name} {verifier.lastname}, 
            Is {auth.first_name} {auth.last_name} a valid researcher in your department?

            Click on the appropriate link to confirm.
            CONFIRM: {request.base_url+ver}
            
    Regards,
    MyEsearch
    """
        verify_author_notif(auth, verifier)
        sendEmail(message, title)
        return True
    else:
        verifier = random.choice(faculty_auths)
        ver = f"/verify/{verifier.id}/{auth_id}"
        message = f"""
    Hi {verifier.first_name} {verifier.lastname}, 
        Is {auth.first_name} {auth.last_name} a vaild researcher in your department?

        Click on the appropriate link to confirm.
        CONFIRM: {request.base_url+ver}
            
    Regards,
    MyEsearch
    """
        verify_author_notif(auth, verifier)
        sendEmail(message,title)
        return True
    return False

def verified(auth_id):
    researcher = Researcher.query.filter_by(id = auth_id).first()
    if researcher:
        try:
            researcher.verify()
            db.session.commit()
            return True
        except:
            return False
    return False