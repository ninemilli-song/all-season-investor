"""
分红
"""
from django.db import models
from .assets import AssetType


class Dividend(models.Model):
    # 基金
    fund = models.OneToOneField(AssetType, on_delete=models.SET_NULL, null=True)
    # 分红时间
    time = models.DateTimeField()
    # 分红金额
    amount = models.FloatField()

    def __str__(self):
        format_time = self.time.strftime('%Y/%m/%d')
        return f'{self.fund.name}-{format_time}-￥{self.amount}'
