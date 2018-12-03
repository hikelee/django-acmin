from django.db import models

from .base import AcminModel


class Alias(AcminModel):
    class Meta:
        abstract = True

    alias = models.CharField("别名", max_length=100)
