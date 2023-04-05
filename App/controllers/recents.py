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
    records = recents[0].records
    records.sort(key=lambda rec: rec.id, reverse=True)
    for rec in records:
        pubs.append(rec.recents_pub) 
    return pubs

def add_publication_to_recents(recents, pub_id):
    for record in recents[0].records:
        if record.publication_id == pub_id:
            remove_publication_from_recents(recents, pub_id)
    if len(recents[0].records) == 20:
        records = recents[0].records
        records.sort(key=lambda rec: rec.id, reverse=True)
        rec = records[-1]
        db.session.delete(rec)
        db.session.commit()
    new_record = RecentsRecord(recents[0].id, pub_id)
    db.session.add(new_record)
    db.session.commit()
    return True

def remove_publication_from_recents(recents, pub_id):
    for record in recents[0].records:
        if record.publication_id == pub_id:
            rec = record
    if not rec:
        return False
    db.session.delete(rec)
    db.session.commit()
    return True

def clear_recents(recents):
    RecentsRecord.query.filter_by(recents_id=recents[0].id).delete()
