from django.db import models

from .base import BaseModel


class Member(BaseModel):
    search_fields = ['name']

    class Gender:
        man = 1
        woman = 0
        chocies = [
            (man, "man"),
            (woman, "woman"),
        ]

    class Meta:
        ordering = ['-id']
        verbose_name = verbose_name_plural = "会员"

    name = models.CharField("名称", max_length=50)
    gender = models.SmallIntegerField(choices=Gender.chocies, default=Gender.woman)

    def __str__(self):
        return self.name
