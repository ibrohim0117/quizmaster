from django.shortcuts import render
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView,
    CreateAPIView, UpdateAPIView,
    DestroyAPIView
)

from .models import Science, Quiz, Answer, Question
from .serializers import (
    ScienceSerializer, QuizSerializer,
    QuestionSerializer, AnswerSerializer
)


class ScienceListAPIView(ListAPIView):
    queryset = Science.objects.all()
    serializer_class = ScienceSerializer


class QuizListAPIView(ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class QuestionListAPIView(ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class AnswerListAPIView(ListAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


