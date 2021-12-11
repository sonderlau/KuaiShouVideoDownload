import json
from threading import main_thread

from rich.pretty import pprint
from utils.GraphQLWrapper import post, request_get_all_videos
from rich.console import Console


# 获取个人所有视频
def get_all_videos(user_id: str, last_update: str, author_name: str):
    """获取所有的视频

    Args:
        user_id (str): 用户id
        last_update (str): 最后更新时间
        author_name (str): 作者名称

    Returns:
        Dict: 视频集合
    """
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

if __name__ == '__main__':
    r = get_all_videos("3x2k7pdreevzzn6", 1638933634482, "把子")
    pprint(r)