from allauth.account import app_settings as allauth_settings
from rest_auth.registration.views import RegisterView
from django.conf import settings
from ..serializers.custom_JWT_serializer import CustomUserJWTSerializer
from rest_auth.app_settings import TokenSerializer
from django.utils.translation import ugettext_lazy as _


class CustomRegisterView(RegisterView):
    def get_response_data(self, user):
        if (
                allauth_settings.EMAIL_VERIFICATION
                == allauth_settings.EmailVerificationMethod.MANDATORY
        ):
            return {"detail": _("Verification e-mail sent.")}

        if getattr(settings, "REST_USE_JWT", False):
            data = {"user": user, "token": self.token}
            return CustomUserJWTSerializer(data, context={"request": self.request}).data
        else:
            return TokenSerializer(
                user.auth_token, context={"request": self.request}
            ).data
