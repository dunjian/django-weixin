#!coding:utf-8
from django.utils.module_loading import autodiscover_modules


def autodiscover():
    """
    自动发现各个app下的signalproc.py 并加载
    """
    autodiscover_modules("signalproc")
