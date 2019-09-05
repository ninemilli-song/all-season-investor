from django.db import models
from .assets import AssetType, Investor


class Initial(models.Model):

    """
    期初数据
    """

    # 基金
    fund = models.OneToOneField(AssetType, on_delete=models.SET_NULL, null=True)
    # 定投开始时间
    start_time = models.DateTimeField()
    # 定投起始金额
    start_amount = models.FloatField()
    # 所有者
    owner = models.ForeignKey(Investor, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.fund.name}[{self.fund.code}]'
