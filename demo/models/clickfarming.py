import datetime

from django.db import models

from .base import BaseModel
from .platform import Platform
from acmin.models import User


class OrderStatus:
    ongoing = 4
    finished = 8
    confirmed = 12

    choices = (
        (ongoing, "正在进行"),
        (finished, "已经结束,等待确认"),
        (confirmed, "已经确认"),
    )


class ClickFarming(BaseModel):
    search_fields = ['platform', 'order_number', 'tracking_number']
    form_exclude = ['reimburse_time']

    class Permission:
        removable = True

    class Meta:
        ordering = ['reimbursed', '-id']
        verbose_name_plural = verbose_name = "刷单"

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="所有者")
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, verbose_name="电商平台")
    order_number = models.CharField("订单号", max_length=50)
    exprense = models.FloatField("刷单费用")
    express_fee = models.FloatField("快递费", default=0)
    tracking_number = models.CharField("快递单号", max_length=30, blank=True, null=True)
    reimbursed = models.BooleanField("已报销?", default=False)
    create_time = models.DateTimeField("创建时间", auto_now_add=True, null=True)
    reimburse_time = models.DateTimeField("报销时间", null=True)

    def save(self):
        if self.reimbursed and not self.reimburse_time:
            self.reimburse_time = datetime.datetime.now()
        super().save()

    def __str__(self):
        return self.order_number

    @property
    def permission(self):
        permission = super().permission
        permission.removable = permission.editable = permission.cloneable = not self.reimbursed

        return permission

    def color(self):
        return "black" if self.reimbursed else "red"
