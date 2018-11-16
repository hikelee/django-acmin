from django.db import models

from .address import Address
from .base import BaseModel
from .book import Book


class Order(BaseModel):
    search_fields = ['name']
    editable = False
    viewable = True

    class Meta:
        ordering = ['-id']
        verbose_name = verbose_name_plural = "订单"

    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    amount = models.FloatField("数量")

    def __str__(self):
        return str(self.id)
