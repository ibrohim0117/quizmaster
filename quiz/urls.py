from django.urls import path
from .views import (
    ScienceListAPIView, QuizListAPIView,
    QuestionListAPIView, OptionListAPIView
)


urlpatterns = [
    path('science/', ScienceListAPIView.as_view(), name='science'),
    path('quiz/', QuizListAPIView.as_view(), name='quiz'),
    path('question/', QuestionListAPIView.as_view(), name='question'),
    path('answer/', OptionListAPIView.as_view(), name='option'),

]
