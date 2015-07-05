#!coding:utf-8
import json
import urllib2
from xml.etree import ElementTree
import pycurl
from cStringIO import StringIO

from django.core.cache import cache

from tmweixin.conf import WeixinConf
from tmweixin.utils.oop import Singleton
from tmweixin.utils.http import client
from tmweixin.exception import WeixinError, WeixinFault

ERROR_CODE_TOKEN = "errcode"


class LazyString(object):
    def __init__(self, source, *args, **kwargs):
        self._source = source
        self._args = args
        self._kwargs = kwargs

    def __str__(self):
        return (self._source % tuple((s() if callable(s) else s for s in self._args))).format(**self._kwargs)


class SimpleApi(object):
    """
    拉取数据型api
    """
    api_url = None
    data_key = None

    def __init__(self, api_url, data_key=None, headers=None, post_data=None):
        self.api_url = api_url
        self.data_key = data_key
        self.headers = headers
        self.post_data = post_data

    def _fetch(self, headers=None, post_data=None):
        json_str = client.open(str(self.api_url), headers or self.headers, post_data or self.post_data).read()
        client.close()
        try:
            result = json.loads(json_str)
        except ValueError:
            raise WeixinFault(u"%s" % json_str)
        err_code = result.get(ERROR_CODE_TOKEN)
        if err_code == 0 or err_code is None:
            self._result = result
            return self._result
        else:
            raise WeixinError(err_code)

    def get_data(self):
        result = self._fetch()
        if self.data_key is None:
            return result
        return result[self.data_key]


class CacheResultApi(SimpleApi):
    """
    使封装的接口能缓存结果
    """
    cache_time = None
    cache_key = None

    def get_data(self, force_update=False):
        """
        @:param force_update:强制更新缓存
        """
        if not all([self.cache_key, self.cache_time]):
            raise NotImplementedError(u"cache_time cache_key should be set")
        data = cache.get(self.cache_key)
        if data is None or force_update:
            result = super(CacheResultApi, self).get_data()
            cache.set(self.cache_key, result, self.cache_time)
            return self.get_data()
        else:
            return data


class UrllibClient(object):
    """使用urlib2发送请求"""

    def __init__(self):
        self.data = None

    def get(self, url, second=30):
        return self.post_xml(None, url, second)

    def post_xml(self, xml, url, second=30):
        """不使用证书"""
        data = urllib2.urlopen(url, xml, timeout=second).read()
        setattr(self, "data", data)
        return data


class CurlClient(object):
    """使用Curl发送请求"""

    def __init__(self):
        self.curl = pycurl.Curl()
        self.curl.setopt(pycurl.SSL_VERIFYHOST, False)
        self.curl.setopt(pycurl.SSL_VERIFYPEER, False)
        # 设置不输出header
        self.curl.setopt(pycurl.HEADER, False)

    def get(self, url, second=30):
        return self.post_xml_ssl(None, url, second=second, cert=False, post=False)

    def post_xml(self, xml, url, second=30):
        """不使用证书"""
        return self.post_xml_ssl(xml, url, second=second, cert=False, post=True)

    def post_xml_ssl(self, xml, url, second=30, cert=True, post=True):
        """使用证书"""
        self.curl.setopt(pycurl.URL, url)
        self.curl.setopt(pycurl.TIMEOUT, second)
        # 设置证书
        # 使用证书：cert 与 key 分别属于两个.pem文件
        # 默认格式为PEM，可以注释
        if cert:
            self.curl.setopt(pycurl.SSLKEYTYPE, "PEM")
            self.curl.setopt(pycurl.SSLKEY, WeixinConf.SSLKEY_PATH)
            self.curl.setopt(pycurl.SSLCERTTYPE, "PEM")
            self.curl.setopt(pycurl.SSLCERT, WeixinConf.SSLCERT_PATH)
        # post提交方式
        if post:
            self.curl.setopt(pycurl.POST, True)
            self.curl.setopt(pycurl.POSTFIELDS, xml)
        buff = StringIO()
        self.curl.setopt(pycurl.WRITEFUNCTION, buff.write)

        self.curl.perform()
        return buff.getvalue()


class HttpClient(Singleton):
    @classmethod
    def configure(cls):
        if pycurl is not None and WeixinConf.HTTP_CLIENT != "URLLIB":
            return CurlClient
        else:
            return UrllibClient


class CommonUtil(object):
    """所有接口的基类"""
    http_client = HttpClient()

    @classmethod
    def array_to_xml(cls, arr):
        """array转xml"""
        xml = ["<xml>"]
        for k, v in arr.iteritems():
            k, v = str(k), str(v)
            if v.isdigit():
                xml.append("<{0}>{1}</{0}>".format(k, v))
            else:
                xml.append("<{0}><![CDATA[{1}]]></{0}>".format(k, v))
        xml.append("</xml>")
        return "".join(xml)

    @classmethod
    def xml_to_array(cls, xml):
        """将xml转为array"""
        array_data = {}
        root = ElementTree.fromstring(xml)
        for child in root:
            value = child.text
            array_data[child.tag] = value
        return array_data

    @classmethod
    def post_xml_curl(cls, xml, url, second=30):
        """以post方式提交xml到对应的接口url"""
        return HttpClient().post_xml(xml, url, second=second)

    @classmethod
    def post_xml_ssl_curl(cls, xml, url, second=30):
        """使用证书，以post方式提交xml到对应的接口url"""
        return HttpClient().post_xml_ssl(xml, url, second=second)


class WeixinBase(CommonUtil):
    """请求型接口的基类"""
    required = ()  # 规定哪些参数必须提供
    response = None  # 微信返回的响应
    url = None  # 接口链接
    curl_timeout = None  # curl超时时间

    def __init__(self, factory, **kwargs):
        self._params_validator = [lambda params, required: all(map(lambda y: y in params, required))]
        self.factory = factory
        self.curl_timeout = factory.timeout
        self.params = self._check_params(kwargs)

    def add_params_validator(self, validator):
        """
        用于增加参数验证方法形如：
            def validator(params, required):
                pass
        """
        self._params_validator.append(validator)

    def _check_params(self, params):
        """
        用于验证参数，默认验证要求的参数是否都具备
        """
        if all([func(params, self.required) for func in self._params_validator]):
            return params
        else:
            raise ValueError(u"参数验证失败")

    def create_xml(self):
        """设置标配的请求参数，生成签名，生成接口参数xml"""
        return self.array_to_xml(self.params)

    def post_xml(self):
        """post请求xml"""
        if self.response is None:
            xml = self.create_xml()
            self.response = self.post_xml_curl(xml, self.url, self.curl_timeout)
        return self.response

    def post_xml_ssl(self):
        """使用证书post请求xml"""
        if self.response is None:
            xml = self.create_xml()
            self.response = self.post_xml_ssl_curl(xml, self.url, self.curl_timeout)
        return self.response

    def get_result_ssl(self):
        """
        使用证书获取结果
        """
        response = self.post_xml_ssl()
        result = self.xml_to_array(response)
        return result

    def get_result(self):
        """获取结果，默认不使用证书"""
        self.post_xml()
        result = self.xml_to_array(self.response)
        return result


