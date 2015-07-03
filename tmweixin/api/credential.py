#!coding: utf-8
"""
接口调用凭据模块
"""
__author__ = 'zkchen'

import json
import datetime
import urllib2

from django.core.cache import cache

from tmweixin.conf import weixin_conf
from tmweixin.exception import WeixinError


ACCESS_TOKEN_CACHE_KEY = "_weixin_access"
SERVER_LIST_CACHE_KEY = "_weixin_server_list"


def get_access_token():
    """
    获取access_token
    """
    app_id = weixin_conf.APPID
    secret = weixin_conf.APPSECRET
    access_token_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' \
                       % (app_id, secret)

    if cache.get(ACCESS_TOKEN_CACHE_KEY) is None:
        # 重新获取token
        req = urllib2.Request(url=access_token_url)
        f = urllib2.urlopen(req)
        json_str = f.read()
        access_token = (json.loads(json_str)).get("access_token", None)
        if access_token is None:
            raise WeixinError(u"%s" % json_str)
        cache.set(ACCESS_TOKEN_CACHE_KEY, access_token, 7000)
    ret = cache.get(ACCESS_TOKEN_CACHE_KEY, None)
    if ret is None:
        raise RuntimeError(u"can't cache access token")
    return ret


# def get_server_ip_list():
#     """  获取微信服务器ip地址列表  """
#     api_url = "https://api.weixin.qq.com/cgi-bin/getcallbackip?access_token=%s" % get_access_token()
#     if cache.get(SERVER_LIST_CACHE_KEY) is None:
#         result = urllib2.urlopen(url=api_url).read()
