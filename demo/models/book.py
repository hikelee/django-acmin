from django.db import models

from .author import Author
from .base import BaseModel


class Book(BaseModel):
    search_fields = ['name']

    class Meta:
        ordering = ['-id']
        verbose_name = verbose_name_plural = "书籍"

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    name = models.CharField("名称", max_length=50)
    price = models.FloatField("价格")
