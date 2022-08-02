from rest_framework import serializers
from ..models import User, Wallet, WalletBalance
from .wallet_serializer import WalletSerializer
from allauth.account.models import EmailAddress


class UserSerializer(serializers.ModelSerializer):
    wallet = serializers.SerializerMethodField()
    is_email_verified = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()
    wallet_balance = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "is_admin",
            "wallet",
            "wallet_balance",
            "is_email_verified",
            "gender",
            "photo",
        ]

    def get_wallet(self, instance):
        try:
            wallet = Wallet.objects.get(user=instance)
            response = WalletSerializer(wallet)
            return response.data
        except Exception as e:
            print("error", e)
            return None

    def get_is_email_verified(self, instance):
        try:
            address = EmailAddress.objects.get(user=instance)
            return address.verified
        except EmailAddress.DoesNotExist:
            return False

    def get_photo(self, instance):
        try:
            return self.context["request"].build_absolute_uri(instance.photo.url)
        except Exception as e:
            print("error", e)
            return None

    def get_wallet_balance(self, instance):
        try:
            balance = WalletBalance.objects.get(user=instance)
            return balance.account_balance
        except Exception as e:
            print("error", e)
            return None
