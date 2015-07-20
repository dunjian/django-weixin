#!coding:utf-8
__author__ = 'akun'
import pickle
from .models import RuntimeConfItem as Item


class RuntimeConf(object):

    def __getattr__(self, name):
        try:
            it = Item.objects.get(key=name)
            return it.value
        except (Item.DoesNotExist, ):
            return None

    def __getitem__(self, item):
        it = self.__getattr__(item)
        if it is None:
            raise KeyError(u"%s doesn't exist" % str(item))
        return it

    def __iter__(self):
        for it in Item.objects.all():
            yield it

