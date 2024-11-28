from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView, status
from .serializers import UserCreateSerializer
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