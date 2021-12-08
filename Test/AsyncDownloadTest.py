# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Sonder Lau
@Version        :  
------------------------------------
@File           :  AsyncDownloadTest.py
@Description    :  
@CreateTime     :  2021/8/18 23:36
------------------------------------
@ModifyTime     :  
"""
from ffmpy3 import FFmpeg
import asyncio

down = "https://v2.kwaicdn.com/upic/2021/08/18/17/BMjAyMTA4MTgxNzE4NDlfMTQzOTU5NTQ5Ml81NTQ5NjM4NDMwNF8xXzM=_b_Bfc93347cf31dde91d8e160ae793e0a51.mp4?pkey=AAUxSsOZdImkgrmASz8jCkfRsUk51wd0iHXyiBU3LC9fIUUxv7XYUZ8DKV90QM_5TLJPeh82JJBrgYvI-ZqQx4pzoloMYBZqf17H4Z7ZCrqtezoLX3LqgfMCvthQhtN3ovE&tag=1-1629367365-xpcwebprofile-0-kpipkcwl0q-be9f2be86713d1c7&clientCacheKey=3xrkuw3q3u9rj3q_b.mp4"


def tt():
    with open('./out.txt', 'w') as log:
        ff = FFmpeg(
            inputs={down: None},
            outputs={'1' + '.mp4': None})
        resp = ff.run(stdout=log)
        print(resp)


if __name__ == '__main__':
    tt()
    # hh = FFmpeg(
    #     inputs={down: None},
    #     outputs={'2' + '.mp4': None})
    #
    # hh .run_async(stdout=log)
    #
    #
    # await hh.wait()
