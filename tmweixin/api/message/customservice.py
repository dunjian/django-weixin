#!coding:utf-8
"""
@desc 客服接口集
@author zkchen (zhongkunchen@126.com)
"""
import hashlib
import json
import urllib2

from tmweixin.api.base import CacheResultPullApi, LazyUrl
from tmweixin.api.credential import AccessToken
from tmweixin.api.decorators import pull_cache_api
from tmweixin.exception import WeixinError


class KFAccount(object):
    """
    客服帐号接口
    """
    CACHE_KF_LIST_KEY = "_kf_list_"

    @pull_cache_api(
        api_klass=CacheResultPullApi,
        api_url=LazyUrl("https://api.weixin.qq.com/cgi-bin/customservice/getkflist?access_token=%s",
                        AccessToken().get_access_token),
        data_key="kf_list",
        cache_time=60,
        cache_key=CACHE_KF_LIST_KEY, )
    def get_kf_list(self, data):
        """ 获取客服列表 """
        return data

    def add_account(self, kf_account, kf_id, nickname, kf_nick=None, password=None):
        """
        添加客服帐号
        :param kf_account: 客服帐号 帐号前缀@公众号微信号
        :param kf_nick: 客服昵称
        :param kf_id: 客服工号
        :param nickname: 客服昵称
        :param password: 32位MD5
        """
        data = {
            "kf_account": kf_account,
            "kf_id": kf_id,
            "nickname": nickname,
        }
        if kf_nick:
            data["kf_nick"] = kf_nick
        if password:
            data["password"] = hashlib.md5(password).hexdigest()
        return self.send_data(url="https://api.weixin.qq.com/customservice/kfaccount/add?access_token=%s" \
                                  % AccessToken().get_access_token(), data=data)

    def update_account(self, kf_account, kf_id=None, nickname=None, kf_nick=None, password=None):
        data = {"kf_account": kf_account}
        if all(k is None for k in [kf_nick, kf_id, nickname, password]):
            return None
        if kf_id:
            data["kf_id"] = kf_id
        if nickname:
            data["nickname"] = nickname
        if kf_nick:
            data["kf_nick"] = kf_nick
        if password:
            data["password"] = hashlib.md5(password).hexdigest()
        return self.send_data(url="https://api.weixin.qq.com/customservice/kfaccount/update?access_token=%s" \
                              % AccessToken().get_access_token(), data=data)

    def send_data(self, url, data):
        result_str = urllib2.urlopen(url, json.dumps(data)).read()
        try:
            result = json.loads(result_str)
        except ValueError:
            raise WeixinError(u"%s" % result_str)
        if result.get("errcode") != 0:
            raise WeixinError(u"%s" % result_str)
        else:
            return result



