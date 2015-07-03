#!coding=utf-8
from tmweixin.send.msg import data_to_xml
from tmweixin.signals import wxsignal_text, wxsignal_image, wxsignal_voice,\
    wxsignal_video, wxsignal_link, wxsignal_location

sender = "tmweixin"


def default_parse_data(msg, data):
    """
    将信号处理器的返回解析并制作成微信消息（xml包）
    :param msg: 微信推送来的消息
    :param data: 信号处理器的返回（列表：[(receiver, response), ..])
    """
    if data and len(data) >= 1:
        for i in range(0, len(data)):
            if data[i][1] is not None:
                return data_to_xml(msg, data[i][1])
    return data_to_xml(msg, {'MsgType': 'text', 'Content': u'功能正在上线中，敬请等待:%s' % str(msg)})


def process_text_msg(msg):
    data = wxsignal_text.send(sender=sender, msg=msg)
    return default_parse_data(msg, data)


def process_image_msg(msg):
    data = wxsignal_image.send(sender=sender, msg=msg)
    return default_parse_data(msg, data)


def process_voice_msg(msg):
    data = wxsignal_voice.send(sender=sender, msg=msg)
    return default_parse_data(msg, data)


def process_video_msg(msg):
    data = wxsignal_video.send(sender=sender, msg=msg)
    return default_parse_data(msg, data)

    
def process_location_msg(msg):
    data = wxsignal_location.send(sender=sender, msg=msg)
    return default_parse_data(msg, data)


def process_link_msg(msg):
    data = wxsignal_link.send(sender=sender, msg=msg)
    return default_parse_data(msg, data)



