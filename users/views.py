from rest_framework.validators import ValidationError
from django.utils import timezone
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView, status
from .serializers import (
    UserCreateSerializer, UserCodeSerializer,
)
from drf_spectacular.utils import extend_schema


class RegisterAPIView(APIView):

    @extend_schema(request=UserCreateSerializer)
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            data = {
                'username': user.username,
                'email': user.email,
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


