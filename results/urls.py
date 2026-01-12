from django.urls import path
from .views import (
    QuizDetailAPIView, SubmitQuizAPIView,
    UserResultsAPIView, ResultDetailAPIView
)

urlpatterns = [
    path('quiz/<int:quiz_id>/', QuizDetailAPIView.as_view(), name='quiz-detail'),
    path('submit/', SubmitQuizAPIView.as_view(), name='submit'),
    path('my-results/', UserResultsAPIView.as_view(), name='my-results'),
    path('result/<int:result_id>/', ResultDetailAPIView.as_view(), name='result-detail'),
]
