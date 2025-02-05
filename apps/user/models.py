from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from apps.user.managers import UserManager
from core.models import BaseModel

class UserModel(AbstractBaseUser, BaseModel):
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
    age = models.IntegerField()
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='profile')
