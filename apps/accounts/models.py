from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

from config import settings


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise TypeError('Email not')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        if not password:
            raise TypeError('password no')
        user = self.create_user(email, password, **extra_fields)
        user.is_supervisor = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, db_index=True)
    first_name = models.CharField(max_length=222, null=True)
    last_name = models.CharField(max_length=222, null=True)
    image = models.ImageField(null=True, blank=True, upload_to='accounts/')
    bio = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_supervisor = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_login = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    objects = AccountManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        if self.first_name:
            return f'{self.first_name}'
        return f'{self.email}'

    @property
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return data


class Team(models.Model):
    name = models.CharField(max_length=222)
    supervisor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tutor', null=True)
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='team_user')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

    @property
    def get_count(self):
        return self.user.count()
