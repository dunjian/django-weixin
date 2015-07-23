#!coding: utf-8
__author__ = 'zkchen'
from tmowx.conf import WeixinConf
from tmowx.api.common import WeixinFactory


weixin_factory = WeixinFactory(WeixinConf.APPID, WeixinConf.MCHID, WeixinConf.KEY)
