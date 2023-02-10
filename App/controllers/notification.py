from App.models import Notification, NotificationRecord
from App.database import db

def create_notification(title, message):
    notification = Notification(title, message)
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

def notify_subscribers(subject, title, message):
    notification = create_notification(title, message)
    for record in subject.sub_records:
        notif = NotificationRecord(record.subscriber.id, notification.id)
        db.session.add(notif)
        db.session.commit()
    return True
