from django.contrib import admin
from django.urls import path, re_path, include
from authentication.views.register_view import CustomRegisterView
from authentication.views.loginview import CustomLoginView
from authentication.views.email_verification_view import verify_user_email
from rest_auth.registration.views import VerifyEmailView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/rest-auth/registration/', CustomRegisterView.as_view(), name="registration"),
    path('api/v1/rest-auth/login/', CustomLoginView.as_view(), name='login'),
    path("verify-email/", verify_user_email, name="verify-email"),
    re_path(r'^account-confirm-email/', VerifyEmailView.as_view(),
            name='account_email_verification_sent'),
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', VerifyEmailView.as_view(),
            name='account_confirm_email'),
    path("api/v1/", include("config.api_router"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

