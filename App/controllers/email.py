import gmail

def sendEmail(message,subject,receipient,html=None,attachments=None):
    try:
        mail = gmail.GMail("somemail.mail.com","mailapppassword")
        msg = gmail.Message(
            subject= subject,
            cc=None,
            to=receipient,
            text=message,
            html=None,
            attachments=None
        )
        mail.send(msg)
        mail.close()
        return True
    except e:
        return False
