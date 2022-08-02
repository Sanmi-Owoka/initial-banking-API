from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from ..models import User
from ..serializers.user_serializer import UserSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class UserViewSet(ModelViewSet):
    model = User
    serializer_class = UserSerializer
    lookup_field = 'id'
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    @action(methods=["PUT"], detail=False, permission_classes=(AllowAny,))
    def editProfile(self, request):
        try:
            user = request.user
            userQS = User.objects.get(id=user.id)
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            gender = request.data['gender']
            photo = request.data['photo']
            if first_name:
                userQS.first_name = first_name.capitalize().strip()
            if last_name:
                userQS.last_name = last_name.capitalize().strip()
            if gender:
                gender_data = gender.capitalize().strip()
                gender_choices = ["Male", "Female"]
                if gender_data not in gender_choices:
                    return Response({
                        "message": f"You entered {gender_data}, our valid gender choices are male and female"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                userQS.gender = gender_data
            if photo:
                userQS.photo = photo
            userQS.save()
            serializer = self.get_serializer(userQS)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print("error", e)
            return Response({"message": [f"{e}"]}, status=status.HTTP_400_BAD_REQUEST)