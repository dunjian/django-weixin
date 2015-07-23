#!coding: utf-8
__author__ = 'zkchen'
from django.db import models
from tmkit import runtask


class Task(models.Model):
    task_name = models.CharField(u"任务名", max_length=250, null=True, blank=True)
    last_response = models.DateTimeField(u"上次应答时间", blank=True, null=True)
    group = models.CharField(u"线程所属任务组", blank=True, null=True, max_length=250)
    thread_ident = models.IntegerField(u"ident")


class TaskLogEntry(models.Model):
    task = models.ForeignKey('Task', verbose_name=u"所属任务")
    content = models.TextField(u"日志", null=True, blank=True)
    log_time = models.DateTimeField(u"时间", auto_now_add=True)
    level = models.CharField(u"级别", choices=((runtask.ERROR, u"错误"), (runtask.DEBUG, u"调试"),
                                             (runtask.INFO, u"信息"), (runtask.WARNING, u"警告")), max_length=100)

