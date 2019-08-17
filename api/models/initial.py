from django.db import models
from .assets import AssetType


class Initial(models.Model):

    """
    期初数据
    """

    # 基金
    found = models.OneToOneField(AssetType, on_delete=models.SET_NULL, null=True)
    # 定投开始时间
    start_time = models.DateTimeField()
    # 定投起始金额
    start_amount = models.FloatField()

    def __str__(self):
        return f'{self.found.name}[{self.found.code}]'
