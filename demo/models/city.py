from django.db import models

from .base import BaseModel


class City(BaseModel):
    from .province import Province
    search_fields = ['province__name', 'name']

    class Meta:
        ordering = ['id']
        verbose_name = verbose_name_plural = "城市"

    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    code = models.CharField("代码", max_length=10)
    name = models.CharField("名称", max_length=150)

    def __str__(self):
        return self.name
