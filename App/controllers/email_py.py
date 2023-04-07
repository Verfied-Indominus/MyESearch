import gmail

# EMAIL : myesearch.noreply@gmail.com
# PASSWORD: admin@noreply
# APP_PASSWORD: sibvelfmfcupbche

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
    except Exception as e:
        return False
