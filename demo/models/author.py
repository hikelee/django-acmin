from django.db import models

from .address import Address
from .base import BaseModel


class Author(BaseModel):
    search_fields = ['name']

    class Meta:
        ordering = ['-id']
        verbose_name = verbose_name_plural = "作者"

    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    name = models.CharField("名称", max_length=50)


    def __str__(self):
        return self.name
    