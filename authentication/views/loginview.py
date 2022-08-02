from django.conf import settings
from ..serializers.custom_JWT_serializer import CustomUserJWTSerializer
from rest_auth.views import LoginView
from rest_auth.app_settings import TokenSerializer


class CustomLoginView(LoginView):
    def get_response_serializer(self):
        if getattr(settings, "REST_USE_JWT", False):
            response_serializer = CustomUserJWTSerializer
        else:
            response_serializer = TokenSerializer
        return response_serializer
