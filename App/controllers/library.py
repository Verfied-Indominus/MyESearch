from App.models import Library, LibraryRecord
from App.controllers.user import get_user
from App.database import db

def create_library(user_id):
    library = Library(user_id)
    db.session.add(library)
    db.session.commit()
    return library

def get_library(id):
    library = Library.query.filter_by(id=id).first()
    return library

def get_library_from_user(id):
    user = get_user(id)
    return user.library

def get_publications_from_library(library):
    pubs = []
    for rec in library[0].records:
        pubs.append(rec.lib_pub)
    return pubs

def add_publication_to_library(library, pub_id):
    for record in library[0].records:
        if record.publication_id == pub_id:
            return False
    new_record = LibraryRecord(library[0].id, pub_id)
    db.session.add(new_record)
    db.session.commit()
    return True

def remove_publication_from_library(library, pub_id):
    for record in library[0].records:
        if record.publication_id == pub_id:
            rec = record
    if not rec:
        return False
    db.session.delete(rec)
    db.session.commit()
    return True

def clear_library(library):
    LibraryRecord.query.filter_by(library_id=library[0].id).delete()
    db.session.commit()