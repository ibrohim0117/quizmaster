from django.contrib import admin
from django.urls import path
from .views import (
    ScienceListAPIView
)


urlpatterns = [
    path('science/', ScienceListAPIView.as_view(), name='science'),

]
