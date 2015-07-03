#!coding:utf-8
"""
@desc 客服接口集
@author zkchen (zhongkunchen@126.com)
"""

from tmweixin.api.base import PullApi, CacheResultMixin

def pull_api(api_klass, api_url, **kwargs):
    pass

class KFAccount(PullApi):
    """
    客服帐号接口
    """
    @pull_api(PullApi, )
    def get_kf_list(self, data):
        return data
