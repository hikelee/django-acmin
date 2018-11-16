from django.db import models

from .base import BaseModel


class Address(BaseModel):
    from .area import Area
    search_fields = ['detail', 'area__name', 'area__city__name', 'area__city__province__name']

    class Meta:
        ordering = ['-id']

    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    detail = models.CharField(max_length=250)
