from django.db import models
from .assets import AssetType, Investor


class InvestRecord(models.Model):
    """
    投资记录
    fund - 基金名称
    data_time - 投资时间
    amount - 投资金额
    """
    fund = models.ForeignKey(AssetType, on_delete=models.SET_NULL, null=True)
    data_time = models.DateTimeField()
    amount = models.FloatField()
    owner = models.ForeignKey(Investor, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.fund} - {self.data_time.strftime("%Y/%m/%d")} - {self.amount}'
