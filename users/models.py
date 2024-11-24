from datetime import timezone, timedelta
import random
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken


class Achievement(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class User(AbstractUser):

    class LevelsTypes(models.TextChoices):
        BEGINNER = '0', 'Beginner'
        ELEMENTARY = '1', 'Elementary'
        INTERMEDIATE = '2', 'Intermediate'
        PRO = '3', 'Pro'

    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(
        upload_to='user/', blank=True, null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
    )
    levels = models.CharField(max_length=255, choices=LevelsTypes.choices, default=LevelsTypes.BEGINNER)
    is_verified = models.BooleanField(default=False)
    ball = models.IntegerField(default=0)
    achievement = models.ManyToManyField(Achievement, blank=True, related_name='users')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

    def update_level(self):
        if self.ball < 200:
            self.levels = self.LevelsTypes.BEGINNER
        elif 200 <= self.ball < 500:
            self.levels = self.LevelsTypes.ELEMENTARY
        elif 500 <= self.ball < 700:
            self.levels = self.LevelsTypes.INTERMEDIATE
        elif 700 <= self.ball < 1000:
            self.levels = self.LevelsTypes.PRO

    def create_code(self):
        code = "".join([str(random.randint(0, 9)) for _ in range(4)])
        UserConfirmation.objects.create(
            code=code,
            user=self.id
        )
        return code

    def token(self):
        refresh = RefreshToken.for_user(self)
        data = {
            "refresh_token": str(refresh),
            "access": str(refresh.access_token)
        }
        return data

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class UserConfirmation(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='codes')
    code = models.CharField(max_length=4)
    expiration_time = models.DateTimeField(default=timezone.now() + timedelta(minutes=10))
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.code




