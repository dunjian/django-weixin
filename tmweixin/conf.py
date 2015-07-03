#!coding: utf-8
__author__ = 'zkchen'


class WeixinConf(object):
    """配置账号信息"""
    # 证书路径,注意应该填写绝对路径
    SSLCERT_PATH = "/apps/cert/apiclient_cert.pem"
    SSLKEY_PATH = "/apps/cert/apiclient_key.pem"
    CURL_TIMEOUT = 30
    HTTP_CLIENT = "CURL"

    APPID = "wx6e513bf6e4c2f17f"
    APPSECRET = "f2ad49affd47b9b6838dfea63b7f7950"
    MCHID = "1229097202"
    KEY = "22bfa596e9aa3295a9ca17330290a25b"


weixin_conf = WeixinConf()
