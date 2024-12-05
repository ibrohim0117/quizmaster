from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


class UserCreateSerializer(ModelSerializer):
    levels = serializers.CharField(read_only=True)
    roles = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'levels', 'roles')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
        )
        user.set_password(validated_data.get('password'))
        user.save()
        user.create_code()
        return user



class UserCodeSerializer(Serializer):
    code = serializers.CharField(write_only=True, max_length=4)


class UserLoginSerializer(Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(username=username, password=password)
        if user and user.is_verified:
            token = RefreshToken.for_user(user)
            data = {
                'username': username,
                'access_token': str(token.access_token),
                'refresh_token': str(token)
            }
            return data
        else:
            raise serializers.ValidationError('Username hato yoki user tasdiqlanmagan')


class UserListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'roles', 'levels')


