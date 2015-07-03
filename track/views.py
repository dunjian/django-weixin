#!coding:utf-8
__author__ = 'akun'
from django.shortcuts import HttpResponse
from track.models import Entry


def raw_response(request):
    """ 使用Entry的id(rid) 查看Entry原始内容 """
    try:
        rid = int(request.GET["rid"])
        entry = Entry.objects.get(pk=rid)
    except (KeyError, ValueError, Entry.DoesNotExist):
        return HttpResponse(u"参数不正确")
    else:
        return HttpResponse(entry.content)
