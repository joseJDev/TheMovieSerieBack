# Django
from django.db import models
from django.contrib.auth.models import AbstractUser

# Utils
from core.base_model import AlternovaModel


class User(AbstractUser, AlternovaModel):
    email = models.EmailField(
        'Email',
        unique=True,
        error_messages={
            'unique': 'Ya existe un usuario con este email.'
        }
    )

    age = models.CharField(
        max_length=5, 
        blank=True, 
        null=True
    )

    profile = models.ImageField(
        upload_to='media/profiles/',
        max_length=255, 
        null=True,
        blank=True
    )
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    class Meta:
        db_table = 'user'
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        