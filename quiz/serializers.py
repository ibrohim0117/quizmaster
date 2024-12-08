from rest_framework.serializers import ModelSerializer, Serializer
from quiz.models import Quiz, Question, Option, Science



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


class OptionSerializer(ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'question', 'option', 'is_true']