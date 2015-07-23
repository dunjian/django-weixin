#!coding: utf-8
"""
接口调用凭据模块
"""
__author__ = 'zkchen'
from django.conf import settings
from django.core.cache import cache

from tmowx.conf import wx_conf
from tmowx.api.base import SimpleApi, CacheResultApi
from tmowx.api.base import LazyString


ACCESS_TOKEN_CACHE_KEY = "_weixin_access"
SERVER_LIST_CACHE_KEY = "_weixin_server_list"
COMPONENT_ACCESS_TOKEN_CACHE_KEY = "owx_access"
COMPONENT_VERIFY_TICKET_CACHE_KEY = "owx_ticket"


class AccessToken(CacheResultApi, SimpleApi):

    cache_key = ACCESS_TOKEN_CACHE_KEY
    cache_time = 7000
    data_key = "access_token"

    def __init__(self):
        api_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' \
                  % (wx_conf.app_id, wx_conf.app_secret)
        super(AccessToken, self).__init__(api_url=api_url, data_key=self.data_key)

    def get_access_token(self):
        return self.get_data()


get_access_token = AccessToken().get_access_token


class ServerList(CacheResultApi, SimpleApi):
    """  获取微信服务器ip地址列表  """
    cache_time = 7 * 24 * 60 * 60
    cache_key = SERVER_LIST_CACHE_KEY
    data_key = "ip_list"

    success_key = (data_key,)
    api_url = LazyString("https://api.weixin.qq.com/cgi-bin/getcallbackip?access_token=%s",
                      AccessToken().get_access_token)

    def get_ip_list(self):
        return self.get_data()


class ComponentAccessToken(CacheResultApi, SimpleApi):
    """
    获取三方平台access_token
    """
    cache_key = COMPONENT_ACCESS_TOKEN_CACHE_KEY
    cache_time = 7000
    data_key = "component_access_token"
    api_url = "https://api.weixin.qq.com/cgi-bin/component/api_component_token"

    def __init__(self):
        super(ComponentAccessToken, self).__init__(api_url=self.api_url, data_key=self.data_key)
        ticket = get_component_ticket()
        assert ticket, u"ticket needed"

        self.post_data = {
            "component_appid": settings.AppId,
            "component_appsecret": settings.AppSecret,
            "component_verify_ticket": ticket
        }


def get_component_ticket():
    return cache.get(COMPONENT_VERIFY_TICKET_CACHE_KEY)
