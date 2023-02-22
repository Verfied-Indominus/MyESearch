from App.models import Publication
from App.database import db
from datetime import date

def create_pub(data): #let data be a dictionary
    try:
        new_pub = Publication(
            title= data["title"],
            abstract= data["abstract"],
            free_access= data["free_access"],
            pub_type=data["pub_type"],
            publication_date=data["pub_date"]

        )
        db.session.add(new_pub)
        db.session.commit()
        return True
    except:
        return False

def update_pub(data,id): #let data be a dictionary
    try:
        query = Publication.query.filter_by(id=id).first()
        query.title = data["title"]
        query.abstract = data["abstract"]
        query.free_access = data["free_access"]
        query.pub_type= data["pub_type"]
        query.publication_date = data['publication_date']
        db.session.commit()
        return True
    except:
        return False

    
def get_pub(title):
    query = Publication.query.filter_by(title=title).first()
    if not query:
        return None
    return query

def get_pub_byid(id):
    query = Publication.query.filter_by(id=id).first()
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
    
def get_all_publications_for_user(user):
    pubs = []
    for rec in user.pub_records:
        pubs.append(rec.publication)
    return pubs