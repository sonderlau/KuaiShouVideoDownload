# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Sonder Lau
@Version        :  
------------------------------------
@File           :  configTest.py
@Description    :  
@CreateTime     :  2021/8/18 21:06
------------------------------------
@ModifyTime     :  
"""
from Configuration.config import *


if __name__ == '__main__':
    print(Configuration().get_video_download_path())
