"""Core models"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)


class UserManager(BaseUserManager):
    """Manages user mapped objects"""

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    STATUS_CHOICES = (
        ('Comensal', 1),
        ('Repartidor', 2),
        ('Administrador', 3)
    )
    status = models.PositiveSmallIntegerField(
        choices=STATUS_CHOICES,
        default=1
    )
    last_login = models.DateTimeField(auto_now_add=True, null=True)
    joined_at = models.DateTimeField(auto_now_add=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'