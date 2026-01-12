from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


class UserCreateSerializer(ModelSerializer):
    levels = serializers.CharField(read_only=True)
    roles = serializers.CharField(read_only=True)
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('email', 'password', 'levels', 'roles')

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Bu email allaqachon ro'yxatdan o'tgan")
        return value

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        
        user = User.objects.create_user(
            email=email,
            password=password,
            username=email  # username ni email bilan to'ldiramiz
        )
        user.create_code()
        return user



class UserCodeSerializer(Serializer):
    code = serializers.CharField(write_only=True, max_length=4)


class UserLoginSerializer(Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('Email yoki parol noto\'g\'ri')
        
        if not user.check_password(password):
            raise serializers.ValidationError('Email yoki parol noto\'g\'ri')
        
        if not user.is_verified:
            raise serializers.ValidationError('Foydalanuvchi tasdiqlanmagan. Iltimos, email orqali kodni tasdiqlang.')
        
        token = RefreshToken.for_user(user)
        data = {
            'email': user.email,
            'access_token': str(token.access_token),
            'refresh_token': str(token)
        }
        return data


class UserListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'roles', 'levels', 'ball')


class UserRatingSerializer(ModelSerializer):
    """Reyting ro'yxati uchun serializer"""
    rank = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'email', 'ball', 'levels', 'rank')


class UserProfileSerializer(ModelSerializer):
    """Foydalanuvchi profili uchun serializer"""
    rank = serializers.SerializerMethodField()
    total_tests = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'email', 'ball', 'levels', 'rank', 'total_tests', 'is_verified', 'created_at')
    
    def get_rank(self, obj):
        """Foydalanuvchining reytingdagi o'rni"""
        users = User.objects.filter(is_active=True).order_by('-ball', 'id')
        rank = 1
        for user in users:
            if user.id == obj.id:
                return rank
            rank += 1
        return None
    
    def get_total_tests(self, obj):
        """Foydalanuvchi ishlagan testlar soni"""
        return obj.results.count()