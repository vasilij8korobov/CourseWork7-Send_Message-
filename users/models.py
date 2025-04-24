from django.contrib.auth.models import AbstractUser
from django.db import models

from config.dry import NULLABLE


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='avatars/', **NULLABLE)
    phone_number = models.CharField(max_length=15, **NULLABLE)
    country = models.CharField(max_length=50, **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
