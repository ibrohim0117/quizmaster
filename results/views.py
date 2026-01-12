from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_spectacular.utils import extend_schema
from .models import Answer, Result
from .serializers import QuizSerializer, SubmitQuizSerializer, ResultSerializer
from quiz.models import Quiz, Option, Question


class QuizDetailAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, quiz_id):
        try:
            quiz = Quiz.objects.prefetch_related('questions__options').get(id=quiz_id)
            serializer = QuizSerializer(quiz)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Quiz.DoesNotExist:
            return Response({"detail": "Quiz topilmadi."}, status=status.HTTP_404_NOT_FOUND)



class SubmitQuizAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @extend_schema(request=SubmitQuizSerializer)
    def post(self, request):
        user = request.user
        serializer = SubmitQuizSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        quiz_id = serializer.validated_data.get('quiz_id')
        answers = serializer.validated_data.get('answers')
        start_time = serializer.validated_data.get('start_time')

        try:
            quiz = Quiz.objects.prefetch_related('questions__options').get(id=quiz_id)
        except Quiz.DoesNotExist:
            return Response({"error": "Test topilmadi"}, status=status.HTTP_404_NOT_FOUND)

        # Testning barcha savollarini olish
        quiz_questions = quiz.questions.all()
        quiz_question_ids = set(quiz_questions.values_list('id', flat=True))
        submitted_question_ids = {answer.get('question_id') for answer in answers}
        
        # Validatsiya: barcha savollar testga tegishli bo'lishi kerak
        if not submitted_question_ids.issubset(quiz_question_ids):
            return Response(
                {"error": "Ba'zi savollar bu testga tegishli emas"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validatsiya: barcha savollarga javob berilishi kerak
        if len(submitted_question_ids) != len(quiz_question_ids):
            return Response(
                {"error": f"Barcha savollarga javob berish kerak. Jami {len(quiz_question_ids)} ta savol, siz {len(submitted_question_ids)} ta javob berdingiz"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validatsiya: har bir savolga faqat bitta javob
        if len(answers) != len(submitted_question_ids):
            return Response(
                {"error": "Har bir savolga faqat bitta javob berish mumkin"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Result yaratish
        result_start_time = start_time if start_time else timezone.now()
        result = Result.objects.create(
            user=user, 
            quiz=quiz,
            start_time=result_start_time
        )

        total_correct = 0
        total_questions = len(quiz_question_ids)

        # Har bir javobni tekshirish va saqlash
        for answer_data in answers:
            question_id = answer_data.get('question_id')
            selected_option_id = answer_data.get('selected_option_id')

            try:
                question = Question.objects.select_related().get(id=question_id, quiz=quiz)
                selected_option = Option.objects.get(id=selected_option_id, question=question)
            except (Question.DoesNotExist, Option.DoesNotExist):
                # Agar savol yoki variant topilmasa, xato javob sifatida saqlaymiz
                continue

            # To'g'ri javobni topish
            correct_option = question.options.filter(is_true=True).first()
            is_correct = selected_option.is_true if selected_option else False

            if is_correct:
                total_correct += 1

            # Javobni saqlash
            Answer.objects.create(
                result=result,
                question=question,
                selected_option=selected_option,
                is_correct=is_correct
            )

        # Natijalarni hisoblash va saqlash
        result.ball = total_correct
        result.end_time = timezone.now()
        result.time_spent_seconds = result.calculate_time_spent()
        result.save()

        # Foydalanuvchi ballini yangilash
        user.ball += total_correct
        user.update_level()
        user.save()

        # To'liq natijani qaytarish
        response_data = ResultSerializer(result).data
        return Response(response_data, status=status.HTTP_200_OK)


class UserResultsAPIView(ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ResultSerializer

    def get_queryset(self):
        return Result.objects.filter(user=self.request.user).select_related('quiz', 'user').prefetch_related(
            'answers__question', 'answers__selected_option', 'answers__question__options'
        ).order_by('-end_time')


class ResultDetailAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, result_id):
        try:
            result = Result.objects.select_related('quiz', 'user').prefetch_related(
                'answers__question', 
                'answers__selected_option',
                'answers__question__options'
            ).get(
                id=result_id, 
                user=request.user
            )
            serializer = ResultSerializer(result)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Result.DoesNotExist:
            return Response({"detail": "Natija topilmadi."}, status=status.HTTP_404_NOT_FOUND)