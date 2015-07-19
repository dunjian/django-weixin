#!coding:utf-8
__author__ = 'akun'
from django.db import models


class Entry(models.Model):
    # request
    path = models.TextField(u"请求路径")
    method = models.CharField(u"方法", max_length=10)
    # TODO：处理文件的问题
    body = models.TextField(u"请求体")
    size = models.IntegerField(u"请求大小(request.body)")
    request_header = models.TextField(u"请求头")
    request_time = models.DateTimeField(u"请求时间")
    # response
    response_header = models.TextField(u"响应头")
    status_code = models.IntegerField(u"返回状态")
    content = models.TextField(u"响应文件内容")
    cost_time = models.IntegerField(u"响应时间(ms)")

    def __unicode__(self):
        return "{path} [{method} {status}] {time} <{cost_time}>".format(
            path=self.path,
            method=self.method,
            time=str(self.request_time),
            status=self.status_code,
            cost_time=self.cost_time
        )

    class Meta:
        verbose_name = u"请求日志"
        verbose_name_plural = u"请求日志管理"

