from django.db import models

from .base import BaseModel


class Province(BaseModel):
    search_fields = ['name']

    class Meta:
        ordering = ['-id']

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
