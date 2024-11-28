from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

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


