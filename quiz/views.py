from django.shortcuts import render
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView,
    CreateAPIView, UpdateAPIView,
    DestroyAPIView
)
from rest_framework.permissions import IsAuthenticated, BasePermission
from django_filters.rest_framework import DjangoFilterBackend
from .models import Science, Quiz, Option, Question
from .serializers import (
    ScienceSerializer, QuizSerializer,
    QuestionSerializer, OptionSerializer
)
from users.models import User


class IsTeacherAndVerified(BasePermission):
    """Faqat Teacher va tasdiqlangan userlar uchun permission"""
    
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.is_verified and
            request.user.roles == User.RolesTypes.TEACHER
        )


class ScienceListAPIView(ListAPIView):
    queryset = Science.objects.all()
    serializer_class = ScienceSerializer



class QuizListAPIView(ListAPIView):
    queryset = Quiz.objects.select_related('science').all()
    serializer_class = QuizSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['degree', 'science_id']



class QuestionListAPIView(ListAPIView):
    queryset = Question.objects.select_related('quiz').all()
    serializer_class = QuestionSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['quiz_id']



class OptionListAPIView(ListAPIView):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer


class QuizCreateAPIView(CreateAPIView):
    """Teacher va tasdiqlangan userlar uchun Quiz yaratish"""
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated, IsTeacherAndVerified]


class QuestionCreateAPIView(CreateAPIView):
    """Teacher va tasdiqlangan userlar uchun Question yaratish"""
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, IsTeacherAndVerified]


class OptionCreateAPIView(CreateAPIView):
    """Teacher va tasdiqlangan userlar uchun Option yaratish"""
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    permission_classes = [IsAuthenticated, IsTeacherAndVerified]

