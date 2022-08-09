import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


def get_avatar_upload_path(instance, filename):
    return f"photos/{instance.email}/{filename}"


class User(AbstractUser):
    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female")
    )
    username = models.CharField(max_length=255, null=True, unique=True)
    gender = models.CharField(max_length=20, null=True, choices=GENDER_CHOICES)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    photo = models.ImageField(null=True, upload_to=get_avatar_upload_path)
    code = models.CharField(max_length=100, null=True, unique=True)
    compromised = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    address = models.CharField(max_length=255, null=True)
    updated_at = models.DateTimeField(auto_now=True)


class Wallet(models.Model):
    TYPE_CHOICES = (
        ("Admin", "Admin"),
        ("Customer", "Customer")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_account')
    unique_code = models.IntegerField(null=True, unique=True)
    type = models.CharField(max_length=100, null=True, default="Customer")
    deactivated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)


class WalletBalance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_balance')
    user_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='wallet_balance')
    account_balance = models.DecimalField(max_digits=15, decimal_places=2)
    credit_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    debit_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)


class TransactionHistory(models.Model):
    TRANSACTION_TYPE_CHOICES = (
        ("Credit", "Credit"),
        ("Debit", "Debit")
    )
    sender_name = models.CharField(max_length=255, null=True)
    sender_email = models.EmailField(max_length=254, null=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    type = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)


class PasswordResetConfirmation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    otp = models.CharField(max_length=10, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)