from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from ..models import User, PasswordResetConfirmation
from ..serializers.user_serializer import UserSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from authentication.utils import send_email
from ..utils import generate_code, validate_email


class UserViewSet(ModelViewSet):
    model = User
    serializer_class = UserSerializer
    lookup_field = 'id'
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    @action(methods=["GET"], detail=False)
    def profile(self, request):
        try:
            user = request.user
            try:
                userQS = User.objects.get(id=user.id)
            except ObjectDoesNotExist:
                return Response({"message": "user does not exist"}, status=status.HTTP_404_NOT_FOUND)
            response = self.get_serializer(userQS)
            return Response(response.data, status=status.HTTP_200_OK)
        except Exception as e:
            print("error", e)
            return Response({"message": [f"{e}"]}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["PUT"], detail=False)
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

    @action(methods=["POST"], detail=False)
    def change_password(self, request):
        try:
            user = request.user
            userQS = User.objects.get(id=user.id)
            old_password = request.data["old_password"]
            password = request.data["password"]
            confirm_password = request.data["confirm_password"]
            if not old_password:
                return Response({"message": "Enter old password"}, status=status.HTTP_400_BAD_REQUEST)
            if not password:
                return Response({"message": "Enter password"}, status=status.HTTP_400_BAD_REQUEST)
            if not confirm_password:
                return Response({"message": "Enter password confirmation"}, status=status.HTTP_400_BAD_REQUEST)
            if not userQS.check_password(old_password):
                return Response({"message": "Invalid Password Entered"}, status=status.HTTP_400_BAD_REQUEST)
            if password != confirm_password:
                return Response({"message": "Password Input does not match"}, status=status.HTTP_400_BAD_REQUEST)
            userQS.set_password(password)
            userQS.save()
            return Response({"message": "Password successfully changed"}, status=status.HTTP_200_OK)
        except Exception as e:
            print("error", e)
            return Response({"message": [f"{e}"]}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["POST"], detail=False,  permission_classes=(AllowAny,))
    def password_reset_request(self, request):
        try:
            email = request.data["email"].strip().lower()
            if not email:
                return Response({"message": "Please enter an email"}, status=status.HTTP_400_BAD_REQUEST)
            if not validate_email(email):
                return Response({"message":f"Invalid email, you entered {email}"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                user = User.objects.get(email=email)
            except ObjectDoesNotExist:
                return Response({"message": f"user with email: {email} does not exist"},
                                status=status.HTTP_404_NOT_FOUND)
            code = generate_code(6)
            resetQS = PasswordResetConfirmation.objects.create(
                user=user,
                otp=code,
            )
            resetQS.save()
            to = user.email
            subject = "Password Reset Confirmation"
            body = f"Hello {user.first_name} {user.last_name}," \
                   f"\n use code: {code} to reset your password"
            data = {"to": to, "subject": subject, "body": body}
            send_email(data)
            return Response({"message": "Check your email for otp code to reset your password"},
                            status=status.HTTP_200_OK)
        except Exception as e:
            print("error", e)
            return Response({"message": [f"{e}"]}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["POST"], detail=False, permission_classes=(AllowAny,))
    def password_reset(self, request):
        try:
            otp = request.data["otp"].strip()
            password = request.data["password"]
            confirm_password = request.data["confirm_password"]
            if not otp:
                return Response({"message": "Please enter an otp"}, status=status.HTTP_400_BAD_REQUEST)
            if not password:
                return Response({"message": "Enter password"}, status=status.HTTP_400_BAD_REQUEST)
            if not confirm_password:
                return Response({"message": "Enter password confirmation"}, status=status.HTTP_400_BAD_REQUEST)
            if password != confirm_password:
                return Response({"message": "Password Input does not match"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                resetQS = PasswordResetConfirmation.objects.get(otp=otp)
            except ObjectDoesNotExist:
                return Response({"message": "Enter a valid otp"}, status=status.HTTP_404_NOT_FOUND)
            user = User.objects.get(email=resetQS.user.email)
            user.set_password(password)
            resetQS.delete()
            user.save()
            return Response({"message": "Password reset successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            print("error", e)
            return Response({"message": [f"{e}"]}, status=status.HTTP_400_BAD_REQUEST)
