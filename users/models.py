from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models

# Create your models here.


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
        INTERMEDIATE = '0', 'Intermediate'
        ELEMENTARY = '0', 'Elementary'

    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(
        upload_to='user/', blank=True, null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
    )
