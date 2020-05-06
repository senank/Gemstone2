from pyramid_mailer.mailer import Mailer
from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message

from ..models import User

def send_email(request):
    mailer = request.mailer

    users = request.dbsession.query(User).all()
    email_lst = []
    for user in users:
        lst.append(user.username)

    message = Message(
        subject = "New Report",
        sender = "senankassem@gmail.com",
        recipients=email_lst,
        body="hi"
        )
    # fsda
    mailer.send_immediately(message, fail_silently = False)