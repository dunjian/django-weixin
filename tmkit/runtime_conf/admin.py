#!coding:utf-8
__author__ = 'akun'
from django.contrib import admin
from .models import *
from django.contrib import messages


class RuntimeConfAdmin(admin.ModelAdmin):
    list_display = ("key", "value", "value_type", "info")
    list_display_links = ("key", )

    def value_type(self, model):
        return type(model.value)

    value_type.short_description = u"值类型"

    # def save_model(self, request, obj, form, change):
    #     try:
    #         raw_value = obj.value
    #         python_value = eval(raw_value)
    #         obj.value = pickle.dumps(python_value)
    #     except SyntaxError as e:
    #         self.message_user(request, e, messages.ERROR)
    #     else:
    #         obj.save()
    #
    # def p_value(self, model):
    #     python_value = pickle.loads(model.value)
    #     return str(python_value)
    #
    # p_value.short_description = u"值"


admin.site.register(RuntimeConfItemProxy, RuntimeConfAdmin)


