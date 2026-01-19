from django.urls import path
from .views import (
    ScienceListAPIView, QuizListAPIView, MyQuizListAPIView,
    QuestionListAPIView, OptionListAPIView,
    QuizCreateAPIView, QuestionCreateAPIView, OptionCreateAPIView
)


urlpatterns = [
    path('science/', ScienceListAPIView.as_view(), name='science'),
    path('quiz/', QuizListAPIView.as_view(), name='quiz'),
    path('quiz/create/', QuizCreateAPIView.as_view(), name='quiz_create'),
    path('quiz/my-quizzes/', MyQuizListAPIView.as_view(), name='my_quizzes'),
    path('question/', QuestionListAPIView.as_view(), name='question'),
    path('question/create/', QuestionCreateAPIView.as_view(), name='question_create'),
    path('answer/', OptionListAPIView.as_view(), name='option'),
    path('answer/create/', OptionCreateAPIView.as_view(), name='option_create'),

]
