from rest_framework import serializers
from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists, get_username_max_length
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from django.utils.translation import ugettext_lazy as _
from uuid import uuid4
from twilio.rest import Client
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from ..models import User


class CustomRegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    phone = serializers.CharField(max_length=17, required=True)

    def validate_username(self, username):
        username = get_adapter().clean_username(username)
        return username

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address.")
                )
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError(
                _("The two password fields didn't match.")
            )
        getPhoneExist = User.objects.filter(phone=data["phone"])
        if getPhoneExist.exists():
            raise serializers.ValidationError(_("User with phone number already exist"))
        return data

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        return {
            "first_name": str(self.validated_data.get("first_name", "")).capitalize(),
            "last_name": str(self.validated_data.get("last_name", "")).capitalize(),
            "password1": self.validated_data.get("password1", ""),
            "email": self.validated_data.get("email", ""),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        user.first_name = str(self.get_cleaned_data()["first_name"]).capitalize()
        user.last_name = str(self.get_cleaned_data()["last_name"]).capitalize()
        user.email = str(self.get_cleaned_data()["email"]).lower()
        user.phone = str(self.get_cleaned_data()["phone"])
        user.category = str(self.get_cleaned_data()["category"])
        user.business_type = str(self.get_cleaned_data()["business_type"])
        user.is_agent = True
        user.compliance = 'Pending'
        user.unique_referral_code = generate_unique_code()
        user.save()
