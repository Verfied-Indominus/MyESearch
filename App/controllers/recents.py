from App.database import db
from App.models.library import Library
from App.models.libraryrecord import LibraryRecord
from App.controllers.user import get_user



def create_recents(user_id):
    recents = Library(user_id)
    db.session.add(recents)
    db.session.commit()
    return recents

def get_recents(id):
    return Library.query.filter_by(id=id).first()

def get_recents_from_user(id):
    user = get_user(id)
    return user.recents

def get_publications_from_recents(recents):
    pubs = []
    for rec in recents[0].records:
        pubs.append(rec.publication)
    return pubs

def add_publication_to_recents(recents, pub_id):
    for record in recents.records:
        if record.publication_id == pub_id:
            return False
    new_record = LibraryRecord(id, pub_id)
    db.session.add(new_record)
    db.session.commit()
    return True

def remove_publication_from_recents(recents, pub_id):
    for record in recents.records:
        if record.publication_id == pub_id:
            pub = record.publication
    if not pub:
        return False
    db.session.delete(pub)
    db.session.commit()
    return True

def clear_recents(recents):
    LibraryRecord.query.filter_by(library_id=recents.id).delete()
