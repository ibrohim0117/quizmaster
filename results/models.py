from django.db import models
from django.utils import timezone
from django.conf import settings
from quiz.models import Quiz, Question, Option

class Result(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='results')
    quiz = models.ForeignKey('quiz.Quiz', on_delete=models.CASCADE, related_name='results')
    ball = models.IntegerField(default=0)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(blank=True, null=True)
    time_spent_seconds = models.IntegerField(default=0, help_text="Vaqt soniyalarda")

    class Meta:
        verbose_name = "Natija"
        verbose_name_plural = "Natijalar"
        ordering = ['-end_time']

    def __str__(self):
        return f"{self.user.email} - {self.quiz.name}"

    @property
    def test_time(self):
        if self.end_time:
            return self.end_time - self.start_time
        return None

    @property
    def total_questions(self):
        return self.quiz.questions.count()

    @property
    def percentage(self):
        """Foizni hisoblaydi"""
        if self.total_questions > 0:
            return round((self.ball / self.total_questions) * 100, 2)
        return 0.0

    def calculate_time_spent(self):
        """Vaqtni soniyalarda hisoblaydi"""
        if self.end_time and self.start_time:
            delta = self.end_time - self.start_time
            return int(delta.total_seconds())
        return 0


class Answer(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey('quiz.Question', on_delete=models.CASCADE, related_name='answers_result')
    selected_option = models.ForeignKey('quiz.Option', on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Javob"
        verbose_name_plural = "Javoblar"

