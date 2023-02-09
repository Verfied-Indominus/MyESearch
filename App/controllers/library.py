from App.models import Library, LibraryRecord
from App.database import db
from sqlalchemy import delete

def create_library(user_id):
    library = Library(user_id)
    return library

def get_library(id):
    library = Library.query.filter_by(id=id).first()
    return library

def add_publication_to_library(library, pub_id):
    for record in library.records:
        if record.publication_id == pub_id:
            return False
    new_record = LibraryRecord(id, pub_id)
    db.session.add(new_record)
    db.session.commit()
    return True

def remove_publication_from_library(library, pub_id):
    for record in library.records:
        if record.publication_id == pub_id:
            pub = record.publication
    if not pub:
        return False
    db.session.delete(pub)
    db.session.commit()
    return True

def clear_library(library):
    LibraryRecord.query.filter_by(library_id=library.id).delete()