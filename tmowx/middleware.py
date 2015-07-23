#!coding: utf-8
__author__ = 'zkchen'
from .api.common import get_openid
from django.shortcuts import HttpResponseRedirect
from django.conf import settings
import urllib
import re
from tmkit.runtime_conf import settings as runtime_settings
from config import PATH_EXCLUDE_LIST_TOKEN, TMWEIXIN_TURN_ON, TMWEIXIN_DEBUG


path_exclude_list = []


class TMWeixinMiddleware(object):
    def __init__(self):
        self.on_key = "debug"
        self.on_value = "off"
        self.force_redirect_token = "err_code"
        self.wf = runtime_settings

    def process_request(self, request):
        exclude_path = runtime_settings.get(PATH_EXCLUDE_LIST_TOKEN) or path_exclude_list
        for p in exclude_path:
            p = re.compile(p)
            if p.match(request.get_full_path()):
                return
        assert hasattr(request, 'session'), (u"session should be available"
                                             u"please add session middleware in settings")
        code = request.GET.get("code", None)
        # 非debug模式下要求必须运行于微信环境
        if code is None and request.session.get("openid", None) is None and not self.wf.get(TMWEIXIN_DEBUG):
            setattr(request, self.force_redirect_token, True)

        elif code is not None and request.session.get("openid", None) is None:
            try:
                request.session["openid"] = get_openid(code)
            except KeyError:
                # code 无效则重新获取
                setattr(request, self.force_redirect_token, True)

    def process_response(self, request, response):
        if getattr(request, self.force_redirect_token, None):
            return HttpResponseRedirect("https://open.weixin.qq.com/connect/oauth2/authorize?"
                                        "appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=1"
                                        "#wechat_redirect" % (settings.WEIXIN_APPID,
                                                              urllib.quote("http://%s%s" % (settings.SITE_HOST,
                                                                                            request.get_full_path()))))
        else:
            return response
