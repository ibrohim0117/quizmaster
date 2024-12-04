from rest_framework.serializers import ModelSerializer, Serializer
from quiz.models import Quiz, Question, Answer, Science



class ScienceSerializer(ModelSerializer):
    class Meta:
        model = Science
        fields = ['id', 'name']


class QuizSerializer(ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'name']


class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question', 'quiz']


class AnswerSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'question', 'answer', 'is_true']