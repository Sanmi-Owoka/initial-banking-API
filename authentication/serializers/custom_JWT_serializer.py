from rest_auth.serializers import JWTSerializer
from django.conf import settings
from rest_auth.utils import import_callable
from .user_serializer import UserSerializer


class CustomUserJWTSerializer(JWTSerializer):
    def get_user(self, obj):
        """
        Required to allow using custom USER_DETAILS_SERIALIZER in
        JWTSerializer. Defining it here to avoid circular imports
        """
        rest_auth_serializers = getattr(settings, "REST_AUTH_SERIALIZERS", {})
        JWTUserDetailsSerializer = import_callable(
            rest_auth_serializers.get("USER_DETAILS_SERIALIZER", UserSerializer)
        )
        user_data = JWTUserDetailsSerializer(obj["user"], context=self.context).data
        return user_data
