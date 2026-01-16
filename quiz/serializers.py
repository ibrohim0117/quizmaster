from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from quiz.models import Quiz, Question, Option, Science



class ScienceSerializer(ModelSerializer):
    class Meta:
        model = Science
        fields = ['id', 'name']


class QuizSerializer(ModelSerializer):
    """Test/Mavzu serializer - Test va Mavzular birlashtirilgan"""
    science_name = serializers.CharField(source='science.name', read_only=True)
    
    class Meta:
        model = Quiz
        fields = ['id', 'name', 'degree', 'science', 'science_name', 'description', 'count_questions']


class QuestionSerializer(ModelSerializer):
    question_name = serializers.CharField(source='question', read_only=True)
    quiz_name = serializers.CharField(source='quiz.name', read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'question', 'question_name', 'quiz', 'quiz_name', 'options']


class OptionSerializer(ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'question', 'option', 'is_true']