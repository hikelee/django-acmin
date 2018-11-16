from django.db import models

from .base import BaseModel


class Member(BaseModel):
    search_fields = ['name']

    class Meta:
        ordering = ['-id']

    name = models.CharField(max_length=50)
