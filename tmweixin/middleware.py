#!coding: utf-8
from django.core.cache import cache
from django.conf import settings
import time
import logging

__author__ = 'zkchen'
from .api.common import get_openid


class TMWeixinMiddleware(object):
    def process_request(self, request):
        code = request.GET.get("code", None)
        if code is not None and request.session.get("openid", None) is None:
            request.session["openid"] = get_openid(code)

        assert hasattr(request, 'user'), (
            "The tmweixin middleware requires authentication middleware."
            "to be installed. Edit your MIDDLEWARE_CLASSES setting."
            "to insert 'django.contrib.auth.AuthenticationMiddleware."
        )

    def process_response(self, request, response):
        if response.status_code == 500:
            con = []
            for r in response:
                con.append(r)
            logging.getLogger(settings.DEBUG_LOGGER).error("".join(con))
        return response
        # if response.status_code == 500:
        #     cache.set("err_500", response)
