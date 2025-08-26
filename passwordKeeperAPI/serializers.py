from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.db import IntegrityError

from passwordKeeperAPI.models import Password

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        try:
            user = User.objects.create_user(**validated_data)
            Token.objects.create(user=user)  # Создаём токен
            return user
        except IntegrityError:
            raise serializers.ValidationError({
                "username": "Пользователь с таким именем уже существует."
            })


class PasswordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Password
        fields = '__all__'


class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Password
        fields = ['site_name', 'login', 'password_text']