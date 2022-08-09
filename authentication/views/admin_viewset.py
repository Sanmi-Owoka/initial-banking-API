from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from ..serializers.user_serializer import UserSerializer
from ..models import User, Wallet
from ..permissions import IsAdmin
from ..utils import validate_email

class AdminViewSet(ModelViewSet):
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "id"
    permission_classes =[IsAdmin]

    # get all users data
    @action(methods=["GET"], detail=False)
    def users(self, request):
        try:
            users = self.queryset
            serializer = self.get_serializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print("error", e)
            return Response({"message": [f"{e}"]}, status=status.HTTP_400_BAD_REQUEST)

    # get specific user data
    @action(methods=["GET"], detail=False)
    def get_user(self, request):
        try:
            email = request.GET.get('email').lower()
            if not email:
                return Response({"message":"No email entered"}, status=status.HTTP_400_BAD_REQUEST)
            if not validate_email(email):
                return Response({"message":f"Invalid email, you entered {email}"}, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.filter(email=email)
            if not user.exists():
                return Response({"message":f"User with {email}, does not exist"}, status=status.HTTP_404_NOT_FOUND)
            userQS = user.first()
            serializer = self.get_serializer(userQS)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print("error", e)
            return Response({"message": [f"{e}"]}, status=status.HTTP_400_BAD_REQUEST)

    # deactivate and activate account
    @action(methods=["POST"], detail=False)
    def user_account(self, request):
        try:
            wallet_number = request.data["wallet_number"]
            deactivate = request.data["deactivate"].lower()
            print(deactivate)
            if not wallet_number:
                return Response({"message": "No wallet number entered"}, status=status.HTTP_400_BAD_REQUEST)
            if not deactivate:
                return Response({"message": "Invalid input for deactivate"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                wallet = Wallet.objects.get(unique_code=wallet_number)
            except ObjectDoesNotExist:
                return Response({"message": f"Wallet with number: {wallet_number} not found"}, status=status.HTTP_404_NOT_FOUND)
            choice = ["true", "false"]
            if deactivate not in choice:
                return Response({"message": "Invalid Input"}, status=status.HTTP_400_BAD_REQUEST)
            print(wallet.user.email)
            
            if deactivate == "true":
                wallet.deactivated = True
                wallet.save()
            if deactivate == "false":
                wallet.deactivated = False
                wallet.save()
            user = User.objects.get(email=wallet.user.email)
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print("error", e)
            return Response({"message": [f"{e}"]}, status=status.HTTP_400_BAD_REQUEST)

    # decativate user wallet
    @action(methods=["POST"], detail=False)
    def deactivate_user_account(self, request):
        try:
            wallet_number = request.GET.get('wallet_number')
            if not wallet_number:
                return Response({"message": "No wallet number entered"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                wallet = Wallet.objects.get(unique_code=wallet_number)
            except ObjectDoesNotExist:
                return Response({"message":f"Wallet with {wallet_number}, does not exist"}, 
                status=status.HTTP_404_NOT_FOUND)
            wallet.deactivated = True
            wallet.save()
            user = User.objects.get(email=wallet.user.email)
            serializer = self.get_serializer(user)
            return Response({"message": "User wallet deactivated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            print("error", e)
            return Response({"message": [f"{e}"]}, status=status.HTTP_400_BAD_REQUEST)

    # activate user wallet
    @action(methods=["POST"], detail=False)
    def activate_user_account(self, request):
        try:
            wallet_number = request.GET.get('wallet_number')
            if not wallet_number:
                return Response({"message": "No wallet number entered"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                wallet = Wallet.objects.get(unique_code=wallet_number)
            except ObjectDoesNotExist:
                return Response({"message":f"Wallet with {wallet_number}, does not exist"}, 
                status=status.HTTP_404_NOT_FOUND)
            wallet.deactivated = False
            wallet.save()
            user = User.objects.get(email=wallet.user.email)
            serializer = self.get_serializer(user)
            return Response({"message": "User wallet activated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            print("error", e)
            return Response({"message": [f"{e}"]}, status=status.HTTP_400_BAD_REQUEST)
