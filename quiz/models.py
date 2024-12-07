from django.db import models


class BaseCreatedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']


class Science(BaseCreatedModel):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Fanlar'
        verbose_name = 'Fan'

    def __str__(self):
        return self.name


class Quiz(BaseCreatedModel):
    class DegreeType(models.TextChoices):
        EASY = '1', 'Easy'
        MEDIUM = '2', 'Medium'
        HARD = '3', 'Hard'

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    degree = models.CharField(max_length=5, choices=DegreeType.choices, default=DegreeType.EASY)
    science = models.ForeignKey(Science, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Tests'
        verbose_name = 'Test'

    def __str__(self):
        return self.name

    @property
    def count_questions(self):
        return Question.objects.filter(quiz=self).count()


class Question(BaseCreatedModel):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question = models.TextField()

    class Meta:
        verbose_name_plural = 'Savollar'
        verbose_name = 'Savol'

    def __str__(self):
        return self.question


class Option(BaseCreatedModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    option = models.TextField()
    is_true = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['question'],
                condition=models.Q(is_true=True),
                name='bitta_savolga_ikki_javob'
            )
        ]
        verbose_name_plural = 'Variantlar'
        verbose_name = 'Variant'

    def __str__(self):
        return self.option


