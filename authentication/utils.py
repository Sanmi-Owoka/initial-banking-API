import yagmail
from django.conf import settings


def send_email(data):
    yag = yagmail.SMTP(user=settings.DEV_EMAIL, password=settings.DEV_PASSWORD)
    yag.send(to=data["to_email"], subject=data["email_subject"], contents=data["email_body"])
