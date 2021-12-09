# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Sonder Lau
@Version        :  
------------------------------------
@File           :  ParseVideoTest.py
@Description    :  
@CreateTime     :  2021/8/18 21:49
------------------------------------
@ModifyTime     :  
"""
from Configuration.GraphQLWrapper import get_video_real_mp4_path,post

if __name__ == '__main__':
    print(post(js= get_video_real_mp4_path("3x4g2b9attf6q9u","3xrkuw3q3u9rj3q")))