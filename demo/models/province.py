from django.db import models

from .base import BaseModel


class Captial:
    captial = 3
    normal = 5

    choices = [
        (captial, "是"),
        (normal, "否")
    ]


class Province(BaseModel):
    search_fields = ['name']

    class Meta:
        ordering = ['id']
        verbose_name = verbose_name_plural = "省份"

    code = models.CharField("代码", max_length=10)
    name = models.CharField("名称", max_length=50)
    is_capital = models.SmallIntegerField("是否首都", choices=Captial.choices, default=Captial.normal)

    def __str__(self):
        return self.name

    @property
    def instance_permission(self):
        permission = super().instance_permission
        return permission
