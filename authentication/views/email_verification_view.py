from rest_framework.response import Response
from rest_framework import status
from allauth.account.models import EmailAddress
from ..models import User
from django.http import HttpResponse


def verify_user_email(request):
    code = request.GET.get("code")
    if not code:
        return HttpResponse("No code entered")
    user = User.objects.filter(code=code)
    if not user.exists():
        return HttpResponse("email verification link invalid")
    userQS = user.first()
    address = EmailAddress.objects.get(user=userQS)
    address.verified = True
    address.primary = True
    address.save()
    return HttpResponse("Welcome to Basic Banking, Your email has been verified")
