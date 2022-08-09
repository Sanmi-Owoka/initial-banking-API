import yagmail
from django.conf import settings
import random
import string
from .models import User, Wallet
from django.core.mail import EmailMessage
import re

def send_email(data):
    email = EmailMessage(
        subject=data['subject'],
        body=data['body'],
        to=[data['to']],
    )
    email.send()


def generate_code(num):
    return ''.join(random.choice(string.digits) for i in range(num))


def generate_unique_code():
    code = generate_code(6)
    exists = User.objects.filter(code=code).exists()
    while exists:
        code = generate_code(6)
        exists = User.objects.filter(code=code).exists()
    return code


def create_account_number(num):
    return '619' + ''.join(random.choice(string.digits) for i in range(num))


def unique_account_number():
    code = create_account_number(6)
    exists = Wallet.objects.filter(unique_code=code).exists()
    while exists:
        code = create_account_number(6)
        exists = Wallet.objects.filter(unique_code=code).exists()
    return code

def validate_email(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  
    if re.search(regex, email):
        return True
    return False
