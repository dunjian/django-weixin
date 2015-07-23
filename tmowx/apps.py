#!coding:utf-8
__author__ = 'akun'
from django.apps import AppConfig
from django.conf import settings


class SimpleWeixinConfig(AppConfig):
    name = 'tmowx'
    verbose_name = u'微信三方平台开发包'


class WeixinConfig(SimpleWeixinConfig):

    def ready(self):
        super(WeixinConfig, self).ready()
        # 自动发现signalproc以注册事件处理器
        self.module.autodiscover()

        for conf in ['AppId', 'AppSecret', 'MessageToken', "EncryptKey"]:
            assert hasattr(settings, conf), u"%s must be set in project settings file" % conf
