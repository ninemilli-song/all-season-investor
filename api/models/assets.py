from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here.


# 安全/安心
# 风险/成长
class Bucket(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    description = models.CharField(max_length=200, null=True, blank=True)
    rate = models.FloatField(null=True)

    def __str__(self):
        return self.name + ' - ' + self.code


# 资产类目
# EX: 股票（股票 基金） 债券 黄金 房地产
class AssetCategory(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    level = models.ForeignKey(Bucket, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class AssetType(models.Model):

    """
    资产品种 具体的基金或者股票
    """

    category = models.ForeignKey(AssetCategory, on_delete=models.SET_NULL, null=True)

    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.name}[{self.code}]'


# 性别
class Sex(models.Model):
    label = models.CharField(max_length=20)
    value = models.CharField(max_length=20)

    def __str__(self):
        return self.label

    def __unicode__(self):
        return self.label


class Investor(models.Model):
    """
    自定义用户模型
    """

    # 用户
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    sex = models.ForeignKey(Sex, on_delete=models.SET_NULL, null=True)
    mobile = models.CharField(max_length=11)

    def __str__(self):
        return self.user.username


class Asset(models.Model):
    """
    资产
    type - 资产品种
    owner - 资产所有者
    pv - 资本现值(Present value)
    principal - 本金
    """
    type = models.ForeignKey(AssetType, on_delete=models.SET_NULL, null=True)
    owner = models.ForeignKey(Investor, on_delete=models.SET_NULL, null=True)
    pv = models.FloatField(default=0)
    principal = models.FloatField(default=0)

    def __str__(self):
        return self.type.name + ' - ' + str(self.pv)


class UserLoginActivity(models.Model):
    """
    Create a model to track login activity
    """
    # Login Status
    SUCCESS = 'S'
    FAILED = 'F'

    LOGIN_STATUS = (
        (SUCCESS, 'Success'),
        (FAILED, 'Failed')
    )

    login_IP = models.GenericIPAddressField(null=True, blank=True)
    login_dateTime = models.DateTimeField(auto_now=True)
    login_username = models.CharField(max_length=40, null=True, blank=True)
    status = models.CharField(max_length=1, default=SUCCESS, choices=LOGIN_STATUS, null=True, blank=True)
    user_agent_info = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'user_login_activity'
        verbose_name_plural = 'user_login_activities'
