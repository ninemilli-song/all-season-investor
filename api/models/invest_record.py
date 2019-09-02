from django.db import models
from .assets import AssetType, Investor


class InvestRecord(models.Model):
    """
    投资记录
    fund - 基金名称
    date_time - 投资时间
    amount - 投资金额
    principal - 当前时间节点下的本金额
    pv - 当前时间节点下的市值
    """
    fund = models.ForeignKey(AssetType, on_delete=models.SET_NULL, null=True)
    date_time = models.DateTimeField()
    amount = models.FloatField()
    owner = models.ForeignKey(Investor, on_delete=models.SET_NULL, null=True)
    principal = models.FloatField(default=0)
    pv = models.FloatField(default=0)

    def __str__(self):
        return f'{self.fund} - {self.date_time.strftime("%Y/%m/%d")} - {self.amount}'
