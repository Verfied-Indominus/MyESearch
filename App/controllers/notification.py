from App.models import Notification, NotificationRecord,Researcher,Student,Publication,PubRecord,Student,Topic,User
from App.database import db
from .email_py import sendEmail
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

def notify_subscribers_author(r_id,pub_id):
    researcher = Researcher.query.filter_by(id = r_id).first()
    subs = researcher.sub_records.all()
    pub = Publication.query.filter_by(id = pub_id).first()
    title = f"New publication by {researcher.first_name} {researcher.last_name}"
    message = f"{researcher.first_name} {researcher.last_name} just released '{pub.title}' "
    notif_title = json.dumps({"name": f"{researcher.title} {researcher.first_name} {researcher.last_name}", "image_url": f"{researcher.image_url}"})
    notif_message = json.dumps({"pub_type": f"{pub.pub_type}", "pub_title": f"{pub.title}"})
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
    notif_message = json.dumps({"pub_type": f"{pub.pub_type}", "pub_title": f"{pub.title}", "contact": contact, "r_id": f"{r_id}", "s_id": f"{s_id}", "pub_id": f"{pub_id}"})
    notif = create_notification(notif_title, notif_message, 2)
    try:
        record = NotificationRecord(r_id, notif.id)
        db.session.add(record)
        db.sesion.commit()
        sendEmail(message + contact,title,researcher.email)
        return True
    except Exception:
        return False

def notify_subscribers_topic(topic_id,pub_id):
    topic = Topic.query.filter_by(id = topic_id).first()
    subs = topic.sub_records
    pub = Publication.query.filter_by(id = pub_id).first()
    title = f"New publication under {topic.name}"
    message = f"New publication '{pub.title}' under the topic '{topic.name}'"
    notification = create_notification(title, message)
    for record in subs:
        notif = NotificationRecord(record.user_id, notification.id)
        user = record.subscriber
        sendEmail(message, title, user.email)
        db.session.add(notif)
        db.session.commit() 
    return True

def reject(s_id,pub_id):
    pub = Publication.query.filter_by(id = pub_id).first()
    title = f"Rejected Request for: '{pub.title}'"
    message = f"This notification is to notify you that the request to access '{pub.title}' has been rejected. "
    student = Student.query.filter_by(id = s_id).first()
    try:
        notif = Notification(title, message)
        db.session.add(notif)
        db.sesion.commit()
        record = NotificationRecord(s_id, notif.id)
        db.session.add(record)
        db.sesion.commit()
        sendEmail(message, title, student.email)
        return True
    except Exception:
        return False

def accept(s_id,pub_id):
    pub = Publication.query.filter_by(id = pub_id).first()
    title = f"Accept Request for: '{pub.title}'"
    message = f"This notification is to notify you that the request to access '{pub.title}' has been granted. "
    student = Student.query.filter_by(id=s_id).first()
    try:
        notif = Notification(title, message)
        db.session.add(notif)
        db.sesion.commit()
        record = NotificationRecord(s_id, notif.id)
        db.session.add(record)
        db.sesion.commit()
        sendEmail(message, title, student.email)
        return True
    except Exception:
        return False

def author_added(p_id,r_id):
    try:
        authors = PubRecord.query.filter_by(publication_id = p_id).all()
        pub = Publication.query.filter_by(id = p_id)
        researcher = Researcher.query.filter_by(id = r_id).first()
        for auth in authors:
            title = "New Researcher Added."
            message = f"this notification is info you that {researcher.first_name} {researcher.last_name} has been added as a author of '{pub.title}'"
            notif = Notification(title, message)
            db.session.add(notif)
            db.sesion.commit()
            record = NotificationRecord(auth.id, notif.id)
            db.session.add(record)
            db.sesion.commit()
            sendEmail(message,title,auth.email)

        return True
    except Exception:
        return False

def verified_notif(auth_id,res_id): 
    auth = Researcher.query.filter_by(id = auth_id).first()
    researcher = Researcher.query.filter_by(id = res_id).first()
    title = f"Verified"
    message = f"You have been verified by {researcher.first_name} {researcher.last_name}."
    try:
        notif = Notification(title, message)
        db.session.add(notif)
        db.sesion.commit()
        record = NotificationRecord(auth_id, notif.id)
        db.session.add(record)
        db.sesion.commit()
        sendEmail(message,title,auth.email)
        return True
    except Exception:
        return False