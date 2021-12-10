import json
from utils.GraphQLWrapper import post, request_get_all_videos
from rich.console import Console


# 获取个人所有视频
def get_all_videos(user_id, last_update, author_name):
    res = post(request_get_all_videos(user_id))

    # 输出 获取到的个人页视频结果
    # console.print(res)

    # 解析JSON
    feeds = json.loads(res)["data"]["visionProfilePhotoList"]["feeds"]

    # 结果 dict
    short_videos = {}
    for feed in feeds:
        # 视频发布时间判断
        if int(last_update) <= int(feed["photo"]["timestamp"]):
            #
            short_videos[feed["photo"]["id"]] = {
                "timestamp": feed["photo"]["timestamp"],
                "author": author_name,
                # 真实下载地址
                "download": feed["photo"]["photoUrls"][0]["url"],
            }
    return short_videos


# 获取主页信息
def get_home_page(id):
    res = post(get_home_page(id))
    print(res)
