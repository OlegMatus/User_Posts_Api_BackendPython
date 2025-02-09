from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from apps.user.managers import UserManager
from core.models import BaseModel


class UserModel(AbstractBaseUser, PermissionsMixin, BaseModel):
    class Meta:
        db_table = 'auth_user'
        ordering = ['id']

    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = UserManager()


class ProfileModel(BaseModel):
    class Meta:
        db_table = 'profile'
        ordering = ['id']

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(null=True, blank=True)
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='profile')
    objects = models.Manager()


class UserSessionModel(models.Model):
    class Meta:
        db_table = 'user_session'

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='user_session')
    session_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Session{self.session_id} for {self.user.email}'
