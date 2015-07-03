#!coding: utf-8
__author__ = 'zkchen'

import urllib2


class Client(object):
    def __init__(self, opener=None, cookies=None):
        self.cookies = cookies or urllib2.HTTPCookieProcessor()
        self.opener = opener or urllib2.build_opener(self.cookies)
        self.request = None
        self.add_info_url = None

    def open(self, url, headers=None, data=None):
        headers = headers or {}
        self.request = urllib2.Request(
            url=url,
            headers=headers,
            data=data
        )
        self.add_info_url = self.opener.open(self.request)
        return self.add_info_url

    def close(self):
        self.add_info_url.close()
        self.opener.close()
        self.cookies.close()


client = Client()