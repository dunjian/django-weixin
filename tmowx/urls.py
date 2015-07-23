#!coding=utf-8
from django.conf.urls import patterns, url

AUTHORIZE_CALLBACK_PATH = "auth_callback"

urlpatterns = patterns('',
                       url(r'^', 'tmowx.views.callback'),
                       url(r'^authCallback', 'tmowx.views.auth_callback', name=AUTHORIZE_CALLBACK_PATH),
                       )
