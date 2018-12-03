from django.db import models

from .base import AcminModel


class AcminContentType(AcminModel):
    class Meta:
        verbose_name_plural = verbose_name = "模型"

    class Permission:
        creatable = editable = removable = cloneable = viewable = False

    name = models.CharField("名称", max_length=100, unique=True)
    verbose_name = models.CharField("描述", max_length=100)

    def __str__(self):
        return f"{self.verbose_name}({self.name})"
