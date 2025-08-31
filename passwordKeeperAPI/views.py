from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import viewsets
from rest_framework import generics
from .models import Password
from passwordKeeperAPI.models import Password
from passwordKeeperAPI.serializers import RegistrationSerializer, PasswordSerializer, PasswordsSerializer
from passwordKeeperAPI.services import Crypto


# Create your views here.
class RegistrationAPIView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutAPIVIew(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AuthStatuAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        is_authenticated = request.user.is_authenticated
        username = request.user.username
        return Response({'is_authenticated': is_authenticated, 'username': username})


class UsersPasswordsAPIView(generics.ListAPIView):
    serializer_class = PasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.passwords.all()


class PasswordsViewSet(viewsets.ModelViewSet):
    queryset = Password.objects.all()
    serializer_class = PasswordsSerializer


class SavePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        site_name = request.data.get('site_name')
        login = request.data.get('login')
        password = request.data.get('password')
        hash_password = Crypto.encrypt(password, request.user.password)
        Password.objects.create(
            site_name=site_name,
            login=login,
            password_text=hash_password,
            user=request.user
        )
        return Response(status=status.HTTP_201_CREATED)

class DeletePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        id = request.data.get('id')
        user = request.user
        Password.objects.filter(pk=id).delete()
