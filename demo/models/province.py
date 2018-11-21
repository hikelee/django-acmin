from django.db import models

from .base import BaseModel


class Province(BaseModel):
    search_fields = ['name']

    class Meta:
        ordering = ['-id']
        verbose_name = verbose_name_plural = "省份"

    name = models.CharField("名称", max_length=50)

    def __str__(self):
        return self.name