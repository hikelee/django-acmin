from django.db import models

from .base import BaseModel


class Platform(BaseModel):
    class Meta:
        verbose_name_plural = verbose_name = "平台"

    name = models.CharField("名称", max_length=20)

    def __str__(self):
        return self.name
