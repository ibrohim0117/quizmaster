from rest_framework import serializers
from quiz.models import Quiz, Question, Option
from .models import Result, Answer


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'option', 'is_true']


class OptionForQuizSerializer(serializers.ModelSerializer):
    """Serializer for quiz taking - hides correct answers"""
    class Meta:
        model = Option
        fields = ['id', 'option']


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'question', 'options']


class QuestionForQuizSerializer(serializers.ModelSerializer):
    """Serializer for quiz taking - hides correct answers"""
    options = OptionForQuizSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'question', 'options']


class QuizSerializer(serializers.ModelSerializer):
    """Serializer for quiz taking - hides correct answers"""
    questions = QuestionForQuizSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'name', 'questions']



class AnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    selected_option_id = serializers.IntegerField()


class SubmitQuizSerializer(serializers.Serializer):
    quiz_id = serializers.IntegerField()
    answers = AnswerSerializer(many=True)
    start_time = serializers.DateTimeField(required=False, help_text="Test boshlanish vaqti")


class WrongAnswerSerializer(serializers.Serializer):
    """Xato javoblar uchun serializer"""
    question_id = serializers.IntegerField()
    question_text = serializers.CharField()
    selected_option_id = serializers.IntegerField()
    selected_option_text = serializers.CharField()
    correct_option_id = serializers.IntegerField()
    correct_option_text = serializers.CharField()


class ResultSerializer(serializers.ModelSerializer):
    total_correct = serializers.SerializerMethodField()
    total_questions = serializers.SerializerMethodField()
    percentage = serializers.SerializerMethodField()
    quiz_name = serializers.CharField(source='quiz.name', read_only=True)
    test_time = serializers.SerializerMethodField()
    time_spent_formatted = serializers.SerializerMethodField()
    wrong_answers = serializers.SerializerMethodField()

    class Meta:
        model = Result
        fields = ['id', 'user', 'quiz', 'quiz_name', 'ball', 'total_correct', 'total_questions', 
                  'percentage', 'start_time', 'end_time', 'test_time', 'time_spent_seconds', 
                  'time_spent_formatted', 'wrong_answers']

    def get_total_correct(self, obj):
        return obj.ball

    def get_total_questions(self, obj):
        return obj.total_questions

    def get_percentage(self, obj):
        return obj.percentage

    def get_test_time(self, obj):
        if obj.test_time:
            return str(obj.test_time)
        return None

    def get_time_spent_formatted(self, obj):
        """Vaqtni formatlangan ko'rinishda qaytaradi"""
        if obj.time_spent_seconds:
            hours = obj.time_spent_seconds // 3600
            minutes = (obj.time_spent_seconds % 3600) // 60
            seconds = obj.time_spent_seconds % 60
            
            if hours > 0:
                return f"{hours} soat {minutes} daqiqa {seconds} soniya"
            elif minutes > 0:
                return f"{minutes} daqiqa {seconds} soniya"
            else:
                return f"{seconds} soniya"
        return None

    def get_wrong_answers(self, obj):
        """Xato javoblar ro'yxatini qaytaradi"""
        wrong_answers = obj.answers.filter(is_correct=False).select_related('question', 'selected_option')
        
        result = []
        for answer in wrong_answers:
            # To'g'ri javobni topish
            correct_option = answer.question.options.filter(is_true=True).first()
            
            if correct_option:
                result.append({
                    'question_id': answer.question.id,
                    'question_text': answer.question.question,
                    'selected_option_id': answer.selected_option.id,
                    'selected_option_text': answer.selected_option.option,
                    'correct_option_id': correct_option.id,
                    'correct_option_text': correct_option.option,
                })
        
        return result
