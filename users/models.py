from datetime import timezone, timedelta
import random
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
# from .tasks import task_send_mail


class UserManager(BaseUserManager):
    """Custom User Manager for email-based authentication"""
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email majburiy maydon')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser is_staff=True bo\'lishi kerak')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser is_superuser=True bo\'lishi kerak')
        
        # username ni email bilan to'ldiramiz
        if not extra_fields.get('username'):
            extra_fields['username'] = email
        
        return self.create_user(email, password, **extra_fields)


class Achievement(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    points = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    sales = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Sovg'alar"
        verbose_name = "Sovg'a"


    def __str__(self):
        return self.name


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()

    class LevelsTypes(models.TextChoices):
        BEGINNER = '0', 'Beginner'
        ELEMENTARY = '1', 'Elementary'
        INTERMEDIATE = '2', 'Intermediate'
        PRO = '3', 'Pro'

    class RolesTypes(models.TextChoices):
        ADMIN = '1', 'Administrator'
        USERS = '2', 'Users'
        SUPPORT = '3', 'Support'

    username = models.CharField(max_length=150, blank=True, null=True, unique=False)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(
        upload_to='user/', blank=True, null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
    )
    levels = models.CharField(max_length=25, choices=LevelsTypes.choices, default=LevelsTypes.BEGINNER)
    roles = models.CharField(max_length=25, choices=RolesTypes.choices, default=RolesTypes.USERS)
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
        code = "".join([str(random.randint(1, 9)) for _ in range(4)])
        # task_send_mail(self.email, code)
        UserConfirmation.objects.create(
            code=code,
            user_id=self.id
        )
        return code

    def token(self):
        refresh = RefreshToken.for_user(self)
        data = {
            "refresh_token": str(refresh),
            "access_token": str(refresh.access_token)
        }
        return data

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


def get_expiration_time():
    return timezone.now() + timedelta(minutes=10)


class UserConfirmation(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='codes')
    code = models.CharField(max_length=4)
    expiration_time = models.DateTimeField(default=get_expiration_time)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.code




