from django.db import models

from .base import BaseModel


class Book(BaseModel):
    from .author import Author
    search_fields = ['name']

    class Meta:
        ordering = ['-id']

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.FloatField()
