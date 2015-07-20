#!coding:utf-8
__author__ = 'akun'
from django.apps import AppConfig


class SimpleWeixinConfig(AppConfig):
    name = 'tmweixin'
    verbose_name = u'微信开发包'


class WeixinConfig(SimpleWeixinConfig):

    def ready(self):
        super(WeixinConfig, self).ready()
        self.module.autodiscover()
