from App.database import db
from App.models.recents import Recents
from App.models.recentsrecord import RecentsRecord
from App.controllers.user import get_user


def create_recents(user_id):
    recents = Recents(user_id)
    db.session.add(recents)
    db.session.commit()
    return recents

def get_recents(id):
    return Recents.query.filter_by(id=id).first()

def get_recents_from_user(id):
    user = get_user(id)
    return user.recents

def get_publications_from_recents(recents):
    pubs = []
    for rec in recents[0].records:
        pubs.append(rec.recents_pub)
    return pubs

def add_publication_to_recents(recents, pub_id):
    for record in recents.records:
        if record.publication_id == pub_id:
            return False
    new_record = RecentsRecord(id, pub_id)
    db.session.add(new_record)
    db.session.commit()
    return True

def remove_publication_from_recents(recents, pub_id):
    for record in recents.records:
        if record.publication_id == pub_id:
            pub = record.recents_pub
    if not pub:
        return False
    db.session.delete(pub)
    db.session.commit()
    return True

def clear_recents(recents):
    RecentsRecord.query.filter_by(recents_id=recents.id).delete()
