from django.db import models

from core.models import BaseModel

from apps.user.models import UserModel


class PostModel(BaseModel):
    class Meta:
        db_table = 'posts'

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=120)
    content = models.TextField(blank=False, null=False)
