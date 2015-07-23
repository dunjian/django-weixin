#!coding=utf-8
import json
import urllib2
from xml.etree import ElementTree

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from tmowx.api.common import check_request
from django.http import HttpResponse, HttpResponseForbidden

from tmowx.api import handlers
from tmowx.api.credential import get_access_token



@csrf_exempt
def auth_callback(request):
    """
    授权回调
    """
    auth_code = request.GET.get("auth_code")
    expires_in = request.GET.get("expires_in")
    if not all([auth_code, expires_in]):
        return HttpResponse("bad request")



def get_subscriber_list():
    """
    #正确时返回JSON数据包：
    #{"total":2,"count":2,"data":{"openid":["","OPENID1","OPENID2"]},"next_openid":"NEXT_OPENID"}
    #This function returns an openid list.

    附：关注者数量超过10000时
    当公众号关注者数量超过10000时，可通过填写next_openid的值，从而多次拉取列表的方式来满足需求。
    具体而言，就是在调用接口时，将上一次调用得到的返回中的next_openid值，作为下一次调用中的next_openid值。
    """
    next_openid = ""
    openid_list = []
    wx_api = "https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s&next_openid=%s" % (
        get_access_token(), next_openid)

    while True:
        ret = json.loads(urllib2.urlopen(wx_api).read())
        print ret
        if ret.get("errcode") is not None:
            return HttpResponseForbidden()
        openid_list.extend(ret.get('data').get('openid'))
        if ret.get("count") != 10000 or ret.get("next_openid") == "":
            return openid_list
    return openid_list


def parse_xml(request):
    if request.body == "":
        echo_str = request.GET.get("echostr", None) or "Nothing"
        return HttpResponse(echo_str)
    msg = {}
    print(request.body)
    xml_elem = ElementTree.fromstring(request.body)
    if xml_elem.tag == 'xml':
        for child in xml_elem:
            msg[child.tag] = child.text
    return msg


@csrf_exempt
def callback(request):
    """
    微信的回调信息
    """
    # not to verify in debug mode
    if not getattr(settings, 'DEBUG'):
        token = getattr(settings, 'WEIXIN_TOKEN')
        if not check_request(request, token):
            return HttpResponse(u'验证失败')

        msg = parse_xml(request)
        msg_type = msg.get("MsgType")
        handle_function = getattr(handlers, "handle_%s" % str(msg_type).lower().strip())

        if callable(handle_function):
            return handle_function(msg)
        else:
            return HttpResponse("XML ERROR")
    else:
        return HttpResponse("BAD MSG")


@csrf_exempt
def accredit(request):
    """
    发起授权页的体验路径
    """


@csrf_exempt
def accredit_event(request):
    """
    授权事件接收逻辑
    """
    msg = parse_xml(request)
    encrypt = msg.get("Encrypt")
    if encrypt is None:
        return HttpResponse("bad request")
    app_id = msg.get("AppId")
    return HttpResponse("SUCCESS")
