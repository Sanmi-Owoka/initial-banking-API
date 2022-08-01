from rest_framework import serializers
from ..models import User, Wallet
from .wallet_serializer import WalletSerializer
from allauth.account.models import EmailAddress


class UserSerializer(serializers.ModelSerializer):
    wallet = serializers.SerializerMethodField()
    is_email_verified = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "is_admin",
            "wallet",
            "is_email_verified"
        ]

    def get_wallet(self, instance):
        try:
            wallet = Wallet.objects.get(user=instance)
            response = WalletSerializer(wallet)
            return response.data
        except:
            return False

    def get_is_email_verified(self, instance):
        try:
            address = EmailAddress.objects.get(user=instance)
            return address.verified
        except EmailAddress.DoesNotExist:
            return False
