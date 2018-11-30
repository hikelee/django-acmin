from django.db import models

from .base import BaseModel
from acmin.models import User


class Expenditure(BaseModel):
    search_fields = ['item']

    class Meta:
        verbose_name_plural = verbose_name = "其他支出"

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="所有者")
    item = models.CharField("事项", max_length=300)
    exprense = models.FloatField("费用")
    reimbursed = models.BooleanField("已报销", default=False)

    def __str__(self):
        return self.item
