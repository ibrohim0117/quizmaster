from django.urls import path
from .views import QuizDetailAPIView

urlpatterns = [
    path('quiz/<int:quiz_id>/', QuizDetailAPIView.as_view(), name='quiz-detail'),
]
