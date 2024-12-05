from django.contrib import admin
from django.urls import path
from .views import (
    RegisterAPIView, UserCodeVerifyAPIView,
    UserLoginAPIView, UserListApiView
)


urlpatterns = [
    path('signup/', RegisterAPIView.as_view(), name='signup'),
    path('login/', UserLoginAPIView.as_view(), name='login'),

    path('code-verify/', UserCodeVerifyAPIView.as_view(), name='code_verify'),

    path('user-list/', UserListApiView.as_view(), name='user_list'),

]
