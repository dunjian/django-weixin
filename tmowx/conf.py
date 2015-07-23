#!coding: utf-8
__author__ = 'zkchen'


# TODO: 使用后端达到settings和admin内均可以配置的效果
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

    @property
    def app_id(self):
        return self.APPID

    @property
    def app_secret(self):
        return self.APPSECRET

    @property
    def mch_id(self):
        return self.MCHID

    @property
    def key(self):
        return self.KEY

    @property
    def timeout(self):
        return self.CURL_TIMEOUT

    @property
    def ssl_key_path(self):
        return self.SSLKEY_PATH

    @property
    def ssl_cert_path(self):
        return self.SSLCERT_PATH


wx_conf = WeixinConf()
