from App.controllers.notification import notify_subscribers_topic
from App.models import Publication, PublicationTag
from App.database import db
from sqlalchemy.exc import IntegrityError

def create_pub(data): #let data be a dictionary
    try:
        new_pub = Publication(
            title= data["title"],
            abstract= data["abstract"],
            free_access= data["free_access"],
            pub_type=data["pub_type"],
            publication_date=data["publication_date"],
            url=data['url'],
            eprint=data['eprint']
        )
        db.session.add(new_pub)
        db.session.commit()
        return new_pub
    except IntegrityError:
        db.session.rollback()
        return None

def add_coauthors(publication, coauthors):
    publication.add_coauthors_string(coauthors)
    db.session.add(publication)
    db.session.commit()
    return True

def update_pub(data,id): #let data be a dictionary
    try:
        query = Publication.query.filter_by(id=id).first()
        query.title = data["title"]
        query.abstract = data["abstract"]
        query.free_access = data["free_access"]
        query.pub_type= data["pub_type"]
        query.publication_date = data['publication_date']
        query.url=data['url']
        query.eprint=data['eprint']
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

def get_all_publications():
    return Publication.query.all()

def get_all_publications_json():
    return [p.toDict() for p in Publication.query.all()]

def get_pub_containing_title(title):
    pub = Publication.query.filter(Publication.title.contains(title)).first()
    if not pub:
        pub = Publication.query.filter(Publication.title.like(title)).first()
    return pub

def add_topic_to_pub(pub, topic):
    try:
        pubtag = PublicationTag(pub.id, topic.id)
        db.session.add(pubtag)
        db.session.commit()
        notify_subscribers_topic(topic.id,pub.id) 
        return True
    except IntegrityError:
        db.session.rollback()
        return False

def add_read_to_pub(pub):
    pub.reads += 1
    db.session.commit()

def add_download_to_pub(pub):
    pub.downloads += 1
    db.session.commit()

def add_citation_to_pub(pub):
    pub.citations += 1
    db.session.commit()

def add_search_to_pub(pub):
    pub.searches += 1
    db.session.commit()

def set_pub_bibtex(pub, bibtex):
    pub.bibtex = bibtex
    db.session.commit()

def set_pub_type(pub, pub_type):
    pub.pub_type = pub_type
    db.session.commit()