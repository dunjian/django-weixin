#!coding:utf-8
__author__ = 'akun'
from django.contrib.admin.sites import site
from .models import *


site.register(Entry)
site.register(Blog)
