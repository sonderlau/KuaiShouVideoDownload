# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Sonder Lau
@Version        :  
------------------------------------
@File           :  PrivateConfig.py
@Description    :  个人配置文件存放处
@CreateTime     :  2021/8/15 13:44
------------------------------------
@ModifyTime     :  
"""

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Cookie": "kpf=PC_WEB; kpn=KUAISHOU_VISION; clientid=3; did=web_7637a1792d22d7ca9884d563a6331cb9; client_key=65890b29; kuaishou.server.web_st=ChZrdWFpc2hvdS5zZXJ2ZXIud2ViLnN0EqABNJUw2LhWE9AwSDkAAAnIPjOzQog47sefgICkA5sQJ7IfH82q6mqeUoLLolh0HeffQhxwKR8Lf6oVM2NybdVW98c5Rtj6J4LuFb38NRxn1XTqICNfacVvx2REuVUgLHNoX4REYXfpBM-Q7j-QCgPcD80hPIMl1D7v29GXaChphnJdUbh4gbEylpo_xamFxaRtMtFbmPA0kb_Na7fhZ2rGeBoSsguEA2pmac6i3oLJsA9rNwKEIiADx__Panna3QRbSX0O_bHh6PQGug8-5I2TNIby-8om3SgFMAE; kuaishou.server.web_ph=248f71e8dc0e318d6935c4cee5bb81374e5b; ktrace-context=1|MS43NjQ1ODM2OTgyODY2OTgyLjMyMTI0NTY1LjE2Mjg1OTg3OTg3MjQuMzM5Mzg2|MS43NjQ1ODM2OTgyODY2OTgyLjQyNTQ2MzY0LjE2Mjg1OTg3OTg3MjQuMzM5Mzg3|0|graphql-server|webservice|false|NA; userId=1477779506",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
}


def get_headers(link=""):
    if link == "":
        return headers
    else:
        headers['Referer'] = link
        return headers


if __name__ == '__main__':
    print(type(get_headers("")))
    print(get_headers(""))
    print(type(get_headers("11123123")))
    print(get_headers("11123123"))