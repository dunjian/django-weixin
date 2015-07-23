#!coding: utf-8
__author__ = 'zkchen'
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from .credential import ComponentAccessToken
from tmowx.urls import AUTHORIZE_CALLBACK_PATH
from tmowx.api.base import SimpleApi, CacheResultApi


class PreAuthCode(CacheResultApi, SimpleApi):
    """
    获取预授权码
    """
    cache_key = "pre_auth_code"
    cache_time = 19 * 60
    data_key = cache_key

    def __init__(self):
        api_url = "https://api.weixin.qq.com/cgi-bin/component/api_create_preauthcode?" \
                  "component_access_token=%s" % ComponentAccessToken().get_data()
        super(PreAuthCode, self).__init__(api_url=api_url, data_key=self.data_key)


class AuthQuery(SimpleApi):
    """
    授权查询
    """
    data_key = None

    def __init__(self, auth_code_value):
        api_url = "https://api.weixin.qq.com/cgi-bin/component/api_query_auth?" \
                  "component_access_token=%s" % ComponentAccessToken().get_data()
        data = {
            "component_appid": settings.AppId,
            " authorization_code": auth_code_value
        }
        super(AuthQuery, self).__init__(api_url=api_url, post_data=data)


def get_authorize_uri(redirect_url=None):
    """
    构造授权网址
    """
    if redirect_url is None:
        assert hasattr(settings, "SITE_HOST"), u"SITE_HOST needed in project settings"
        redirect_url = "http://%s%s" % (settings.SITE_HOST, reverse_lazy(AUTHORIZE_CALLBACK_PATH, args=()))
    return "https://mp.weixin.qq.com/cgi-bin/componentloginpage?" \
           "component_appid=%s" \
           "&pre_auth_code=%s" \
           "&redirect_uri=%s" % (settings.AppId, PreAuthCode().get_data(), redirect_url)
