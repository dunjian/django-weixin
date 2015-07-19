#!coding:utf-8
__author__ = 'akun'
from django.db import models


class RuntimeConfItem(models.Model):
    """
    运行时配置信息
    """
    key = models.CharField(u"键", max_length=250, help_text=u"最长250", primary_key=True, unique=True)
    value = models.CharField(u"配置值", max_length=250, null=True, blank=True, help_text=u"最长250")
    info = models.TextField(u"配置说明", null=True, blank=True)

    class Meta:
        verbose_name = u"运行时配置"
        verbose_name_plural = u"运行时配置管理"

    def __unicode__(self):
        return "%s=>%s" % (self.key, self.value)