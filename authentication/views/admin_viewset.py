from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from ..serializers.user_serializer import UserSerializer
from ..models import User
from ..permissions import IsAdmin
from ..utils import validate_email

class AdminViewSet(ModelViewSet):
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "id"
    permission_classes =[IsAdmin]

    @action(methods=["GET"], detail=False)
    def users(self, request):
        users = self.queryset
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False)
    def get_user(self, request):
        email = request.GET.get('email')
        if not email:
            return Response({"message":"No email entered"})
        if not validate_email(email):
            return Response({"message":f"Invalid email, you entered {email}"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(email=email)
        if not user.exists():
            return Response({"message":f"User with {email}, does not exist"}, status=status.HTTP_404_NOT_FOUND)
        userQS = user.first()
        serializer = self.get_serializer(userQS)
        return Response(serializer.data, status=status.HTTP_200_OK)

    