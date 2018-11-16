from django.db import models

from .base import BaseModel


class Address(BaseModel):
    from .area import Area
    search_fields = ['detail', 'area__name', 'area__city__name', 'area__city__province__name']

    class Meta:
        ordering = ['-id']
        verbose_name = verbose_name_plural = "地址"

    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    detail = models.CharField("详细地址", max_length=250)

    def __str__(self):
        return self.detail
