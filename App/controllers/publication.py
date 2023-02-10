from App.models import publication
from App.database import db

def create_pub(data): #let data be a dictionary
    try:
        new_pub = publication(
            title= data["title"],
            abstract= data["abstract"],
            free_access= data["free_access"],
            library_id= data["library_id"]
        )
        db.session.add(new_pub)
        db.session.commit()
        return True
    except:
        return False

def update_pub(data):
    pass # need to find out if this can actually be changed

def get_pub(name):
    query = publicaton.query.filter_by(title=name).first()
    if not query:
        return None
    return query

def get_pub_byid(id):
    query = publicaton.query.filter_by(id=id).first()
    if not query:
        return None
    return query

def delete_pub(id):
    try:
        pub = get_pub_byid(id)
        db.session.delete(pub)
        db.session.commit()
        return True
    except:
        return  False
