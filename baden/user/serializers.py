from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

from .custom_auth import AuthBackend

User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'login'
    login = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        login = attrs.get("login")
        password = attrs.get("password")

        if login and password:
            user = self.authenticate_user(login, password)
            if user:
                refresh = self.get_token(user)
                data = {}
                data['refresh'] = str(refresh)
                data['access'] = str(refresh.access_token)
                return data
            else:
                raise serializers.ValidationError("Unable to log in with provided credentials.")
        else:
            raise serializers.ValidationError("Must include 'login' and 'password'.")

    def authenticate_user(self, login, password):
        user = AuthBackend().authenticate(request=None, login=login, password=password)
        return user


class UserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'phone_number', 'first_name', 'last_name', 'photo', 'password')
