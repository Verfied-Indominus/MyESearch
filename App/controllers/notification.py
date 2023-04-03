from App.models import Notification, NotificationRecord,Researcher,Student,Publication,PubRecord,Student,Topic,User
from App.database import db
from .email_py import sendEmail
from flask import request
import json

def create_notification(title, message, type):
    notification = Notification(title, message, type)
    db.session.add(notification)
    db.session.commit()
    return notification

def get_notification(id):
    return Notification.query.get(id)

def update_notification_title(id, title):
    notification = get_notification(id)
    if not notification:
        return False
    notification.title = title
    db.session.add(notification)
    db.session.commit()
    return True

def update_notification_message(id, message):
    notification = get_notification(id)
    if not notification:
        return False
    notification.message = message
    db.session.add(notification)
    db.session.commit()
    return True

def delete_notification(id):
    notification = get_notification(id)
    if not notification:
        return False
    db.session.delete(notification)
    db.session.commit()
    return True

# Create notifications to display in notification section in header
# Types:
#     1 - New publication added by a researcher
#     2 - User requests access to a publication
#     3 - Peer Verification
#     4 - New publication under a specific topic
#     5 - Student follows a researcher
#     6 - Researcher follows another researcher
#     7 - Researcher follows back the previous researcher
#     8 - Researcher adds another researcher to publication
#     9 - Researcher accepted access request
#    10 - Researcher rejected access request
#    11 - Researcher has been verified

def notify_subscribers_author(r_id,pub_id):
    researcher = Researcher.query.filter_by(id = r_id).first()
    subs = researcher.sub_records.all()
    pub = Publication.query.filter_by(id = pub_id).first()
    title = f"New publication by {researcher.first_name} {researcher.last_name}"
    message = f"{researcher.first_name} {researcher.last_name} just released '{pub.title}' "
    notif_title = json.dumps({"researcher_id": f"{researcher.id}", "name": f"{researcher.title} {researcher.first_name} {researcher.last_name}", "image_url": f"{researcher.image_url}"})
    notif_message = json.dumps({"pub_id": f"{pub.id}", "pub_type": f"{pub.pub_type}", "pub_title": f"{pub.title}"})
    notification = create_notification(notif_title, notif_message, 1)
    for record in subs:
        notif = NotificationRecord(record.user_id, notification.id)
        user = record.subscriber
        sendEmail(message, title, user.email)
        db.session.add(notif)
        db.session.commit()
    return True

def request_access(s_id,r_id,pub_id,message):
    pub = Publication.query.filter_by(id = pub_id).first()
    student = Student.query.filter_by(id = s_id).first()
    researcher = Researcher.query.filter_by(id = r_id).first()
    title = f"Publication Request: '{pub.title}'"
    contact = f"""Student Details:
                Name: {student.first_name} {student.last_name}
                Email: {student.email} """
    notif_title = json.dumps({"image_url": f"{student.image_url}", "name": f"{student.first_name} {student.last_name}"})
    notif_message = json.dumps({"pub_type": f"{pub.pub_type}", "pub_title": f"{pub.title}", "contact": contact, "r_id": f"{r_id}", "s_id": f"{s_id}", "pub_id": f"{pub_id}", "message": f"{message}"})
    notif = create_notification(notif_title, notif_message, 2)
    try:
        record = NotificationRecord(r_id, notif.id)
        db.session.add(record)
        db.sesion.commit()
        sendEmail(message + contact,title,researcher.email)
        return True
    except Exception:
        return False

def verify_author_notif(re, verifier):
    notif_title = json.dumps({"researcher_id": f"{re.id}", "name": f"{re.title} {re.first_name} {re.last_name}", "image_url": f"{re.image_url}"})
    notif = create_notification(notif_title, "{}", 3)
    try:
        record = NotificationRecord(verifier.id, notif.id)
        db.session.add(record)
        db.session.commit()
        return True
    except Exception:
        return False

def notify_subscribers_topic(topic_id,pub_id):
    topic = Topic.query.filter_by(id = topic_id).first()
    subs = topic.sub_records
    pub = Publication.query.filter_by(id = pub_id).first()
    title = f"New publication under {topic.name}"
    message = f"New publication '{pub.title}' was added under the topic '{topic.name}'"
    notif_title = json.dumps({"pub_id": f"{pub.id}", "pub_title": f"{pub.title}", "pub_type": f"{pub.pub_type}", "topic_id": f"{topic.id}", "topic_name": f"{topic.name}"})
    notification = create_notification(notif_title, "{}", 4)
    for record in subs:
        notif = NotificationRecord(record.user_id, notification.id)
        sendEmail(message, title, record.subscriber.email)
        db.session.add(notif)
        db.session.commit() 
    return True

def student_subscription_notif(r_id, s_id):
    researcher = Researcher.query.filter_by(id=r_id).first()
    student = Student.query.filter_by(id=s_id).first()
    notif_title = json.dumps({"name": f"{student.first_name} {student.last_name}", "image_url": f"{student.image_url}"})
    title = "New Follower"
    message = f"A student has recently followed you: {student.first_name} {student.last_name}"
    notification = create_notification(notif_title, "{}", 5)
    try:
        record = NotificationRecord(researcher.id, notification.id)
        sendEmail(message, title, researcher.email)
        db.session.add(record)
        db.session.commit()
        return True
    except Exception:
        return False
    
def researcher_subscription_notif(re_id, sub_id):
    re = Researcher.query.filter_by(id=re_id).first()
    subscriber = Researcher.query.filter_by(id=sub_id).first()
    notif_title = json.dumps({"researcher_id": f"{subscriber.id}", "name": f"{subscriber.title} {subscriber.first_name} {subscriber.last_name}", "image_url": f"{subscriber.image_url}"})
    title = "New Researcher Follower"
    message = f"""
    A fellow researcher has recently followed you: {subscriber.title} {subscriber.first_name} {subscriber.last_name}
    Click the link below if you would like to return the follow:
    {request.base_url + f"/followback/{re.id}/{subscriber.id}"}
    """
    notification = create_notification(notif_title, "{}", 6)
    try:
        record = NotificationRecord(re.id, notification.id)
        sendEmail(message, title, re.email)
        db.session.add(record)
        db.session.commit()
        return True
    except Exception:
        return False

def follow_back_researcher(re_id, sub_id):
    re = Researcher.query.filter_by(id=re_id).first()
    subscriber = Researcher.query.filter_by(id=sub_id).first()
    notif_title = json.dumps({"researcher_id": f"{re.id}", "name": f"{re.title} {re.first_name} {re.last_name}", "image_url": f"{re.image_url}"})
    title = "A researcher has followed you back"
    message = f"{re.title} {re.first_name} {re.last_name} has reciprocated your follow request"
    notification = create_notification(notif_title, "{}", 7)
    try:
        record = NotificationRecord(subscriber.id, notification.id)
        sendEmail(message, title, subscriber.email)
        db.session.add(record)
        db.session.commit()
        return True
    except Exception:
        return False
    
def author_added(p_id, r_id):
    authors = PubRecord.query.filter_by(publication_id = p_id).all()
    pub = Publication.query.filter_by(id = p_id)
    re = Researcher.query.filter_by(id = r_id).first()
    title = "New Researcher Added."
    notif_title = json.dumps({"researcher_id": f"{re.id}", "name": f"{re.title} {re.first_name} {re.last_name}", "image_url": f"{re.image_url}"})
    notif_message = json.dumps({"pub_id": f"{pub.id}", "pub_type": f"{pub.pub_type}", "pub_title": f"{pub.title}"})
    message = f"This notification is to inform you that {re.title} {re.first_name} {re.last_name} has added you as a co-author of '{pub.title}'"
    notif = create_notification(notif_title, notif_message, 8)
    try:
        for auth in authors:
            if auth.researcher_id != re.id:
                record = NotificationRecord(auth.researcher_id, notif.id)
                db.session.add(record)
                db.sesion.commit()
                sendEmail(message, title, auth.researcher.email)
        return True
    except Exception:
        return False
    
def accept(s_id,pub_id):
    pub = Publication.query.filter_by(id = pub_id).first()
    title = f"Accept Request for: '{pub.title}'"
    message = f"This notification is to notify you that the request to access '{pub.title}' has been granted. The Researcher may contact you via email."
    notif_title = json.dumps({})
    notif_message = json.dumps({"pub_id": f"{pub.id}", "pub_type": f"{pub.pub_type}", "pub_title": f"{pub.title}"})
    student = Student.query.filter_by(id=s_id).first()
    notif = create_notification(notif_title, notif_message, 9)
    try:
        record = NotificationRecord(s_id, notif.id)
        db.session.add(record)
        db.sesion.commit()
        sendEmail(message, title, student.email)
        return True
    except Exception:
        return False

def reject(s_id,pub_id):
    pub = Publication.query.filter_by(id = pub_id).first()
    title = f"Rejected Request for: '{pub.title}'"
    message = f"This notification is to notify you that the request to access '{pub.title}' has been rejected."
    notif_title = json.dumps({})
    notif_message = json.dumps({"pub_id": f"{pub.id}", "pub_type": f"{pub.pub_type}", "pub_title": f"{pub.title}"})
    student = Student.query.filter_by(id = s_id).first()
    notif = create_notification(notif_title, notif_message, 10)
    try:
        record = NotificationRecord(s_id, notif.id)
        db.session.add(record)
        db.sesion.commit()
        sendEmail(message, title, student.email)
        return True
    except Exception:
        return False

def verified_notif(auth_id, res_id): 
    auth = Researcher.query.filter_by(id = auth_id).first()
    re = Researcher.query.filter_by(id = res_id).first()
    title = f"Verified"
    message = f"You have been verified by {re.first_name} {re.last_name}."
    notif_title = json.dumps({"researcher_id": f"{re.id}", "name": f"{re.title} {re.first_name} {re.last_name}", "image_url": f"{re.image_url}"})
    notif = create_notification(notif_title, "{}", 11)
    try:
        record = NotificationRecord(auth_id, notif.id)
        db.session.add(record)
        db.sesion.commit()
        sendEmail(message,title,auth.email)
        return True
    except Exception:
        return False

def set_notif_rec_read(notif_rec_id):
    notif_rec = NotificationRecord.query.filter_by(id=notif_rec_id).first()
    notif_rec.setRead()
    db.session.commit()

def delete_all_notif_recs(user):
    for rec in user.notification_records:
        db.session.delete(rec)
        db.session.commit()
    return True