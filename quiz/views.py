from django.shortcuts import render
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView,
    CreateAPIView, UpdateAPIView,
    DestroyAPIView
)
from django_filters.rest_framework import DjangoFilterBackend
from .models import Science, Quiz, Option, Question
from .serializers import (
    ScienceSerializer, QuizSerializer,
    QuestionSerializer, OptionSerializer
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


