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

    class Meta:
        verbose_name = "Natija"
        verbose_name_plural = "Natijalar"
        ordering = ['-end_time']

    def __str__(self):
        return f"{self.user.username}"

    @property
    def test_time(self):
        if self.end_time:
            return self.end_time - self.start_time
        return None

    @property
    def total_questions(self):
        return self.quiz.questions.count()


