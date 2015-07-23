#!/usr/bin/env python
# -*- coding: utf-8 -*-
from WXBizMsgCrypt import WXBizMsgCrypt

if __name__ == "__main__":
    """
   1.第三方回复加密消息给公众平台；
   2.第三方收到公众平台发送的消息，验证消息的安全性，并对消息进行解密。
   """
    encodingAESKey = "7ab418658a04c9afaab71131cb2416474bf64e1ata1"
    token = "d938d9ebf18881668f8953b176b78648"
    appid = "wxfe0bf88d3d500557"
    # 测试解密接口
    nonce = "706623570"
    timestamp = "1437568224"
    msg_sign = "666bfe8d678c02e5e3e18340ad20a9f2600870f6"

    from_xml = """<xml> <AppId><![CDATA[hhh]]></AppId> <Encrypt><![CDATA[qSyWlYBPiwfoxgubnKjwQvuCvMs3mFzLq6m5HUij/oJmM5U2WLB5gfTmLVngqSww4UdP1Kasu3XQDtr/3rKXF32Z41OO57DTptv3WnxdxCa1VmUnBb0nd2wJ8N4a6WNf1aAKNcGreoikIbSQ9nwRXqzqLDjvb2WNhsvyP8SYTtVcCKC3/6ZjLLH5vV8lA13zrC7zB3xr0S6sBuBM4HJ4WmmGe03/dh8l02Oa8HLksW+lif4PJfGOSDH4XM8pyHechz6qvxvf/99w6yGpGhgZ0nnFbQguaYSzeVBmF6OTn3JuZ6g5ncfj8kGo32BnOB/Lj38yrRtQAfBlBswbmg7Z1pzl0waWsd9efXC+SofQ53o46Dyu+nKpxAXFrVBGYL4qWfFrMq12lC0oFfZ1ET0ZjbROq2wHdiuqDA6gGB59s8kqsnoY0+jnJ2FHoz2RVxzC2pzvuv0x2pnMXF5a96fzsw==]]></Encrypt> </xml> """
    decrypt_test = WXBizMsgCrypt(token, encodingAESKey, appid)
    ret, decryp_xml = decrypt_test.DecryptMsg(from_xml, msg_sign, timestamp, nonce)
    print ret, decryp_xml
