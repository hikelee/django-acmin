from django.db import models

from .base import BaseModel



class Area(BaseModel):
    from .city import City
    search_fields = ['province__name', 'name']

    class Meta:
        ordering = ['-id']

    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
