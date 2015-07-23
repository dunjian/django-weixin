#!coding: utf-8
__author__ = 'zkchen'


class WeixinError(Exception):
    """
    接口调用失败
    """


class ClientError(Exception):
    """
    接口调用发起端的错误
    """


class NetworkError(Exception):
    """
    与微信交互时产生的网络错误
    """


class WeixinFault(Exception):
    """
    微信服务器错误
    """
