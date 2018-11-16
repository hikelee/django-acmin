from django.db import models

from .base import BaseModel


class Area(BaseModel):
    from .city import City
    search_fields = ['province__name', 'name']

    class Meta:
        ordering = ['-id']
        verbose_name = verbose_name_plural = "地区"

    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField("名称", max_length=50)

    def __str__(self):
        return self.name
