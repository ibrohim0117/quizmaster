from django.contrib import admin
from django.urls import path
from .views import (
    RegisterAPIView, UserCodeVerifyAPIView,
)


urlpatterns = [
    path('signup/', RegisterAPIView.as_view(), name='signup'),
    path('code-verify/', UserCodeVerifyAPIView.as_view(), name='code_verify'),

]
