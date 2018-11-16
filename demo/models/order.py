from django.db import models

from .base import BaseModel


class Order(BaseModel):
    from .book import Book
    from .address import Address
    search_fields = ['name']

    class Meta:
        ordering = ['-id']

    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    amount = models.FloatField()
