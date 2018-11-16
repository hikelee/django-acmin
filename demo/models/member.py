from django.db import models

from .base import BaseModel


class Member(BaseModel):
    search_fields = ['name']

    class Meta:
        ordering = ['-id']
        verbose_name = verbose_name_plural = "会员"

    name = models.CharField("名称", max_length=50)
