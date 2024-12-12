from django_filters import filters
from rest_framework.views import APIView
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_spectacular.utils import extend_schema
from .models import Answer, Result
from .serializes import QuizSerializer, SubmitQuizSerializer, ResultSerializer
from quiz.models import Quiz, Option, Question


class QuizDetailAPIView(APIView):

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

        if serializer.is_valid():
            quiz_id = serializer.validated_data.get('quiz_id')
            answers = serializer.validated_data.get('answers')


            try:
                quiz = Quiz.objects.get(id=quiz_id)
            except Quiz.DoesNotExist:
                return Response({"error": "Test topilmadi"}, status=status.HTTP_404_NOT_FOUND)


            result = Result.objects.create(user=user, quiz=quiz)

            total_correct = 0


            for answer_data in answers:
                question_id = answer_data.get('question_id')
                selected_option_id = answer_data.get('selected_option_id')

                try:

                    question = Question.objects.get(id=question_id, quiz=quiz)
                    selected_option = Option.objects.get(id=selected_option_id, question=question)
                except (Question.DoesNotExist, Option.DoesNotExist):
                    continue


                is_correct = selected_option.is_true
                if is_correct:
                    total_correct += 1


                Answer.objects.create(
                    result=result,
                    question=question,
                    selected_option=selected_option,
                    is_correct=is_correct
                )


            result.ball = total_correct
            result.end_time = timezone.now()
            result.save()


            response_data = ResultSerializer(result).data
            return Response(response_data, status=status.HTTP_200_OK)


        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
