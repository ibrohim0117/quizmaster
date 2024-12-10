from django.urls import path
from .views import QuizDetailAPIView, SubmitQuizAPIView

urlpatterns = [
    path('quiz/<int:quiz_id>/', QuizDetailAPIView.as_view(), name='quiz-detail'),
    path('submit/', SubmitQuizAPIView.as_view(), name='submit'),
]
