#!coding: utf-8
__author__ = 'zkchen'
from base import WeixinBase


class UnifiedOrder(WeixinBase):
    """统一下单"""
    url = "https://api.mch.weixin.qq.com/pay/unifiedorder"

    def __init__(self, factory, **kwargs):
        super(UnifiedOrder, self).__init__(factory=factory, **kwargs)

    def get_prepay_id(self):
        return self.get_result()["prepay_id"]

    def get_code_url(self):
        return self.get_result()["code_url"]


class OrderQuery(WeixinBase):
    """订单查询接口"""
    url = "https://api.mch.weixin.qq.com/pay/orderquery"

    def __init__(self, factory, **kwargs):
        super(OrderQuery, self).__init__(factory=factory, **kwargs)
        if all([kwargs.get("out_trade_no") is None, kwargs.get("transaction_id") is None]):
            raise ValueError(u"out_trade_no and transaction_id is None at same time")

    def trade_state(self):
        """
        订单状态
        """
        if self.communication_success() and self.get_result().get("result_code") == "SUCCESS":
            return self.get_result().get("trade_state")

    def communication_success(self):
        """ 与微信接口通信成功否  """
        return self.get_result().get("return_code") == "SUCCESS"


class CloseOrder(WeixinBase):
    """关闭订单"""
    required = ("out_trade_no", )
    url = "https://api.mch.weixin.qq.com/pay/closeorder"


class Refund(WeixinBase):
    """退款申请接口"""
    url = "https://api.mch.weixin.qq.com/secapi/pay/refund"


class RefundQuery(WeixinBase):
    """退款查询接口"""
    url = "https://api.mch.weixin.qq.com/pay/refundquery"

    def get_result(self):
        """ 获取结果，使用证书通信(需要双向证书)"""
        self.post_xml_ssl()
        result = self.xml_to_array(self.response)
        return result


class DownloadBill(WeixinBase):
    """对账单接口"""
    url = "https://api.mch.weixin.qq.com/pay/downloadbill"




