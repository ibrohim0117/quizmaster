from rest_framework import serializers
from .models import Quiz, Question, Option, Result

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'option', 'is_true']


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'question', 'options']


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'name', 'questions']



class AnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    selected_option_id = serializers.IntegerField()


class SubmitQuizSerializer(serializers.Serializer):
    quiz_id = serializers.IntegerField()
    answers = AnswerSerializer(many=True)


class ResultSerializer(serializers.ModelSerializer):
    total_correct = serializers.SerializerMethodField()
    total_questions = serializers.SerializerMethodField()

    class Meta:
        model = Result
        fields = ['quiz', 'ball', 'total_correct', 'total_questions']

    def get_total_correct(self, obj):
        return obj.ball

    def get_total_questions(self, obj):
        return obj.quiz.questions.count()