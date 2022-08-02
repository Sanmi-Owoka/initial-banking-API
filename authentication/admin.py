from django.contrib import admin
from .forms import UserCreationForm, UserChangeForm
from django.contrib.auth import admin as auth_admin
from .models import User, Wallet, WalletBalance


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
                    (
                        "Avatar  info",
                        {"fields": ('gender', 'compromised', 'is_admin', 'address', 'photo')},
                    ),
                ) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", "email", "first_name", "last_name", "is_superuser", "code"]
    list_display_links = ["email", "username"]
    search_fields = ["email", "first_name", "last_name"]


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "unique_code", "type", "created_at", "updated_at"]
    list_display_links = ["user"]
    list_filter = ["type"]
    search_fields = ["user__email"]


@admin.register(WalletBalance)
class WalletBalanceAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "user_wallet", "account_balance", "created_at", "updated_at"]
    list_display_links = ["user"]
    search_fields = ["user__email", "user_wallet__unique_code"]
