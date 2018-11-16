from django.db import models

from .base import BaseModel


class Author(BaseModel):
    from .address import Address
    search_fields = ['name']

    class Meta:
        ordering = ['-id']

    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
