from rest_framework.generics import ListAPIView
from rest_framework.validators import ValidationError
from django.utils import timezone
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView, status

from .models import User
from .serializers import (
    UserCreateSerializer, UserCodeSerializer, UserLoginSerializer, 
    UserListSerializer, UserRatingSerializer, UserProfileSerializer
)
from drf_spectacular.utils import extend_schema


class RegisterAPIView(APIView):

    @extend_schema(request=UserCreateSerializer)
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            data = {
                'email': user.email,
                'message': 'Ro\'yxatdan o\'tdingiz. Email orqali kod yuborildi.',
                'access_token': user.token()['access_token'],
                'refresh_token': user.token()['refresh_token'],
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCodeVerifyAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(request=UserCodeSerializer)
    def post(self, request):
        user = request.user
        serializer = UserCodeSerializer(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data.get('code')
            # print(user, code)
            self.check_verify_code(user, code)
            return Response(
                data={
                    'success': True,
                    'access': user.token()['access_token'],
                    'refresh': user.token()['refresh_token']
                }
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @staticmethod
    def check_verify_code(user, code):
        verify_code = user.codes.filter(code=code, expiration_time__gte=timezone.now(), is_confirmed=False)
        if not verify_code.exists():
            data = {
                'success': False,
                'message': "Code xato yoki eskirgan"
            }
            raise ValidationError(data)
        user.is_verified = True
        verify_code.update(is_confirmed=True)
        user.save()
        return user

class UserLoginAPIView(APIView):

    @extend_schema(request=UserLoginSerializer)
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListApiView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class RatingListView(ListAPIView):
    """Platforma bo'yicha reyting ro'yxati"""
    permission_classes = (AllowAny,)
    serializer_class = UserRatingSerializer
    
    def get_queryset(self):
        # Ball bo'yicha tartiblangan foydalanuvchilar
        users = User.objects.filter(is_active=True).order_by('-ball', 'id')
        # Har bir foydalanuvchiga rank qo'shamiz
        result = []
        for rank, user in enumerate(users, start=1):
            user.rank = rank
            result.append(user)
        return result


class UserProfileView(APIView):
    """Foydalanuvchi profili va reytingi"""
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

