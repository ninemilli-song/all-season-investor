from django.db import models
import json
from django.contrib.auth.models import User

# Create your models here.


# 安全/安心
# 风险/成长
class Bucket(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)

    def __str__(self):
        return self.name + ' - ' + self.code


# 资产品类
# EX: 股票（股票 基金） 债券 黄金 房地产
class AssetCategory(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    bucket = models.ForeignKey(Bucket, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


# 资产类型
# ex：上证50 沪深300 格力电器 伊利股份
class AssetType(models.Model):
    type = models.ForeignKey(AssetCategory, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# 性别
class Sex(models.Model):
    label = models.CharField(max_length=20)
    value = models.CharField(max_length=20)

    def __str__(self):
        return self.label

    def __unicode__(self):
        return self.label


# 用户
class Investor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    sex = models.ForeignKey(Sex, on_delete=models.SET_NULL, null=True)
    mobile = models.CharField(max_length=11)

    def __str__(self):
        return self.name


# 资产
# type - 资产类型
# owner - 资产所有者
# amount - 资产金额
class Asset(models.Model):
    type = models.ForeignKey(AssetType, on_delete=models.SET_NULL, null=True)
    owner = models.ForeignKey(Investor, on_delete=models.SET_NULL, null=True)
    amount = models.FloatField(default=0)


    def __str__(self):
        return self.type.name + ' - ' + str(self.amount)

