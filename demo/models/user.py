from django.contrib.auth.models import AbstractUser
from django.db import models

from acmin.models import ModelMixin


class User(ModelMixin, AbstractUser):
    class Meta:
        ordering = ['-id']
        verbose_name_plural = verbose_name = "用户"

    creatable = editable = removable = True
    list_fields = form_fields = search_fields = ['username', 'title']

    title = models.CharField('名称', max_length=50, blank=False, null=False)

    def __str__(self):
        return self.title
