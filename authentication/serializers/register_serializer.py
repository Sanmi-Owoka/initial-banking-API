from rest_framework import serializers
from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from django.utils.translation import ugettext_lazy as _
from ..utils import generate_unique_code, send_email, unique_account_number
from ..models import Wallet, WalletBalance
from rest_auth.registration.serializers import RegisterSerializer


class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)

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
        return data

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
        user.first_name = str(self.get_cleaned_data()["first_name"]).capitalize().strip()
        user.last_name = str(self.get_cleaned_data()["last_name"]).capitalize().strip()
        user.email = str(self.get_cleaned_data()["email"]).lower().strip()
        user.save()
        code = generate_unique_code()
        user.code = code
        user.save()
        to = user.email
        subject = "EMAIL VERIFICATION"
        body = f"Hello {user.first_name} {user.last_name}," \
               f"\n Verify your email with this link: http: http://127.0.0.1:8000/verify-email/?code={code} "
        data = {"to": to, "subject": subject, "body": body}
        send_email(data)
        try:
            wallet = Wallet.objects.filter(user=user)
            if wallet.exists():
                pass
            wallet = Wallet.objects.create(
                user=user,
                unique_code=unique_account_number(),
                type='Customer'
            )
            wallet.save()
            print('Wallet successfully created')
        except Exception as e:
            print("error", e)
            pass
        try:
            wallet_balance = WalletBalance.objects.create(
                user=user,
                user_wallet=wallet,
                account_balance=0
            )
            wallet_balance.save()
        except Exception as e:
            print("error", e)
            pass
        return user
