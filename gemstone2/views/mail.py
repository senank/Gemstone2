from pyramid_mailer.mailer import Mailer
from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message

def send_email(request):
    mailer = request.mailer

    # users = request.dbsession.query(User).filter(User.)

    message = Message(
        subject = "New Report",
        sender = "senankassem@gmail.com",
        recipients=["senankassem@gmail.com"],
        body="hi"
        )
    # fsda
    mailer.send_immediately(message, fail_silently = False)