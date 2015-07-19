#!coding:utf-8
__author__ = 'akun'

from functools import update_wrapper

from django.conf.urls import patterns, url
from django.contrib.admin.sites import site
from django.shortcuts import HttpResponse
from django.contrib.admin import ModelAdmin
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse_lazy
from django.utils import html

from .models import Entry


class EntryAdmin(ModelAdmin):
    list_display = ("path", "method", "status_code", "request_time", "cost_time", "body_btn")

    def get_urls(self):
        """
        重载路由
        """
        meta = getattr(self.model, "_meta")
        info = meta.app_label, meta.model_name

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)

            return update_wrapper(wrapper, view)

        urlpatterns = patterns(
            '',
            url(r'^$', wrap(self.changelist_view), name='%s_%s_changelist' % info),
            url(r'^(.+)/history/$', wrap(self.history_view), name='%s_%s_history' % info),
            url(r'^(.+)/delete/$', wrap(self.delete_view), name='%s_%s_delete' % info),
            url(r'^(\d+)/$', wrap(self.change_view), name='%s_%s_change' % info),
            url(r'^(\d+)/body/$', wrap(self.view_body), name='%s_%s_body' % info),
        )
        return urlpatterns

    def view_body(self, request, entry_id):
        """
        查看body数据
        """
        entry = self.model.objects.get(pk=int(entry_id))
        return HttpResponse(html.escape(entry.body))

    def readonly_view(self, request, object_id, extra_context=None):
        """
        以只读方式查看记录
        """
        entry = self.model.objects.get(pk=int(object_id))
        return HttpResponse("%s" % entry.content)

    def body_btn(self, model):
        """
        为存在body数据的记录添加查看按钮
        """
        meta = getattr(self.model, "_meta")
        info = meta.app_label, meta.model_name
        body = model.body
        ret = body and mark_safe("<a href={path} >查看</a>".format(
            path=reverse_lazy("admin:%s_%s_body" % info, args=(model.pk, ), kwargs={})
        )) or u""
        return ret
    body_btn.short_description = mark_safe(u"body")
    body_btn.allow_tags = True

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """
        重写“修改”视图为只读
        """
        return self.readonly_view(request, object_id, extra_context)


site.register(Entry, EntryAdmin)
