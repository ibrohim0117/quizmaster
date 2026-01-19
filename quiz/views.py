from django.shortcuts import render
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView,
    CreateAPIView, UpdateAPIView,
    DestroyAPIView
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from .models import Science, Quiz, Option, Question
from .serializers import (
    ScienceSerializer, QuizSerializer,
    QuestionSerializer, OptionSerializer
)
from .permissions import IsTeacherAndVerified


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
    
    def perform_create(self, serializer):
        """Teacher'ni avtomatik qo'shish"""
        serializer.save(teacher=self.request.user)


class MyQuizListAPIView(ListAPIView):
    """Teacher'ning o'zi yaratgan quiz'lari"""
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated, IsTeacherAndVerified]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['degree', 'science_id']
    
    def get_queryset(self):
        """Faqat o'zi yaratgan quiz'larni qaytarish"""
        return Quiz.objects.filter(teacher=self.request.user).select_related('science', 'teacher')


class QuestionCreateAPIView(CreateAPIView):
    """Teacher va tasdiqlangan userlar uchun Question yaratish"""
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, IsTeacherAndVerified]
    
    def perform_create(self, serializer):
        """Faqat o'zi yaratgan quiz'ga Question qo'shish"""
        quiz = serializer.validated_data.get('quiz')
        if quiz.teacher != self.request.user:
            raise PermissionDenied("Siz faqat o'zingiz yaratgan quiz'lar uchun savol qo'sha olasiz.")
        serializer.save()


class OptionCreateAPIView(CreateAPIView):
    """Teacher va tasdiqlangan userlar uchun Option yaratish"""
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    permission_classes = [IsAuthenticated, IsTeacherAndVerified]
    
    def perform_create(self, serializer):
        """Faqat o'zi yaratgan quiz'ga Option qo'shish"""
        question = serializer.validated_data.get('question')
        if question.quiz.teacher != self.request.user:
            raise PermissionDenied("Siz faqat o'zingiz yaratgan quiz'lar uchun variant qo'sha olasiz.")
        serializer.save()

