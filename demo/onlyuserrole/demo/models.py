from django.db import models

# Create your models here.
class RoleDemo(models.Model):
    id = models.AutoField('主键',primary_key=True)
    name = models.CharField('姓名',max_length=20)
    mobile = models.CharField('手机号码',max_length=11)
    address = models.CharField('地址',max_length=100)
    idcord = models.EmailField('身份证号码',max_length=18)
    owner = models.CharField('拥有我', max_length=24)
    organization = models.CharField('拥有我', max_length=24, blank=True)
