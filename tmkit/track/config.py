#!coding: utf-8
__author__ = 'zkchen'
from tmkit.runtime_conf import settings as runtime_settings

TRACK_TURN_ON = runtime_settings.register_key("track.turn_on", u"track模块开关，True表示启用， False为关闭", default=True)