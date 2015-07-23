#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# Author: jonyqin
# Created Time: Thu 11 Sep 2014 03:55:41 PM CST
# File Name: demo.py
# Description: WXBizMsgCrypt 使用demo文件
#########################################################################
from WXBizMsgCrypt import WXBizMsgCrypt
if __name__ == "__main__":   
   """ 
   1.第三方回复加密消息给公众平台；
   2.第三方收到公众平台发送的消息，验证消息的安全性，并对消息进行解密。
   """
   encodingAESKey = "7ab418658a04c9afaab71131cb2416474bf64e1ata1"
   # to_xml = """ <xml><ToUserName><![CDATA[oia2TjjewbmiOUlr6X-1crbLOvLw]]></ToUserName><FromUserName><![CDATA[gh_7f083739789a]]></FromUserName><CreateTime>1407743423</CreateTime><MsgType>  <![CDATA[video]]></MsgType><Video><MediaId><![CDATA[eYJ1MbwPRJtOvIEabaxHs7TX2D-HV71s79GUxqdUkjm6Gs2Ed1KF3ulAOA9H1xG0]]></MediaId><Title><![CDATA[testCallBackReplyVideo]]></Title><Descript  ion><![CDATA[testCallBackReplyVideo]]></Description></Video></xml>"""
   token = "d938d9ebf18881668f8953b176b78648"
   nonce = "1310969867"
   appid = "wxfe0bf88d3d500557"
   #测试加密接口
   # encryp_test = WXBizMsgCrypt(token,encodingAESKey,appid)
   # ret,encrypt_xml = encryp_test.EncryptMsg(to_xml,nonce)
   # print ret,encrypt_xml
   

   #测试解密接口
   timestamp = "1437544825"
   msg_sign  = "8227d295b9372a7cd3ca364253fc627129f61c0a"
   
   from_xml = """<xml> <AppId><![CDATA[wxfe0bf88d3d500557]]></AppId> <Encrypt><![CDATA[RX//QuHb40FYbrnp5MjTZRMpc4ng4Dg5kOYbZhwBI0WueHs0bqktwK8n7JONvUpFK73hjWDjBTW+Pn80Dwlvj7wN1qaaRxFgqNpNqCQgfIOvqMHYM9nuJRIj88RaNwfDKrMtFZvaNaSp1E7b3H5Qbl+Fy0DXOBqWAQwpMMxnL39SLDmjGj21S0W7TImF2Ia+GPCUAybAs509lSvC0Byk8R+dhC8hxZM/GLpumMQCrmRx3HwRl4uKKxpczkJA0fwkwl79PK9fYmSNlSmRO1PpqfTOXjlERxvN6Nlol4x3uDtHqNqwx7u89MFj1jV7kGZx8Lcx84Ybh0mrqBiUU1FTluSWc5SLzsOu5WvsnkoMadux3Pz5Cbprvi+h6pUVThM3jZKFGX12stvWnRuFwkUOa/Lw94BxEbnzmfTzbV3f+3tHuB9JST9wNsEuCF2+rJrs923cbATxrrjRpoo9YMV/Rg==]]></Encrypt> </xml> """
   decrypt_test = WXBizMsgCrypt(token,encodingAESKey,appid)
   ret ,decryp_xml = decrypt_test.DecryptMsg(from_xml, msg_sign, timestamp, nonce)
   print ret ,decryp_xml
