#!coding:utf-8
__author__ = 'akun'
from .models import RuntimeConfItem as Item


class RuntimeConf(object):
    def __getattr__(self, name):
        pass


