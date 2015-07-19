#!coding:utf-8
__author__ = 'akun'

from django.apps import AppConfig


class TrackConfig(AppConfig):
    name = 'tmkit.track'
    verbose_name = u"请求跟踪"
    label = "track"
