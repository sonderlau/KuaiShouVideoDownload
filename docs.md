entrance.py

```python
import json
import os
from collections import defaultdict
from concurrent.futures import ALL_COMPLETED, ThreadPoolExecutor, wait

from icecream import ic
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from rich import print
from rich.pretty import pprint
from rich.progress import Progress

from config.config import Configuration
from src.GetVideoIndex import get_all_videos
from src.MergeVideoFile import merge_video_files
from src.ParseDownload import download_short_video
from utils.TimestampCalculate import target_timestamp

config = Configuration()

# 整理
tasks = defaultdict(list)

with open("./config/subscription.json", "r") as fp:
    questions = json.load(fp)

    choices = []

    # json 文件内容解析
    for k, v in questions.items():
        choices.append(Separator())

        cnt = 0
        for dv in v:
            choices.append(
                Choice(
                    {
                        "name": dv["name"],
                        "value": [
                            dv["value"],
                            # ? 所属分类
                            k,
                            # ? 所在位置
                            cnt,
                        ],
                    },
                    name=dv["name"],
                    enabled=dv["checked"],
                )
            )
            cnt += 1

    answers = inquirer.checkbox(
        message="😃 请选择要下载的视频",
        choices=choices,
        cycle=False,
        # todo: 分类\总个数统计
        transformer=lambda result: "已选择 : {} 个".format(len(result)),
    ).execute()

    # 全部设置为 False
    for k, v in questions.items():
        for one in v:
            one["checked"] = False

    # 选择的选项设置为 True
    for _ in answers:
        category = _["value"][1]
        index = _["value"][2]
        questions[category][index]["checked"] = True

        # 分类
        tasks[category].append(_)

    # 写入
    with open("./config/subscription.json", "w") as fp:
        json.dump(questions, fp)


# 指定下载的时间

print(":baby_chick: 请输入你想抓取的视频发布起始日期\n:computer_disk:格式：[bold cyan]13d / 1m[/bold cyan]")

# 计算目标时间戳
timestamp = target_timestamp(inquirer.text(message="请输入: ").execute())

# 以 类别 为任务单位 分配下载任务

for category, _ in tasks.items():

    # ? 线程池
    with ThreadPoolExecutor() as pool:
        thread_pool_list = []
        for one in _:
            # 获取作者的主页视频
            print(":downwards_button:当前下载目标：{}".format(one["name"]))
            videos = get_all_videos(one["value"][0]["id"], timestamp, one["name"])
            # 此作者的 所有待下载视频个数
            for each_video_k, each_video_v in videos.items():
                # 提交一个视频的下载
                print(":fast_down_button:正在下载：{} - {}".format(category, each_video_v["author"]))
                task_pool = pool.submit(
                    download_short_video,
                    each_video_v["download"],
                    each_video_v["timestamp"],
                    each_video_v["author"],
                    category,
                )

                thread_pool_list.append(task_pool)

        wait(thread_pool_list, return_when=ALL_COMPLETED)
        print(":doughnut:下载完成!")
        # 以 类别 位单位 合并每个分类内的视频
    with open(
        config.get_video_download_path() + category + ".in",
        mode="w+",
        encoding="utf-8",
    ) as ff:
        # 清空文件内容
        ff.write("")

    with open(
        config.get_video_download_path() + category + ".in",
        mode="a",
        encoding="utf-8",
    ) as ff:
        # 遍历 属于当前分类的 mp4 文件
        for root, ds, fs in os.walk(config.get_video_download_path()):
            for filename in fs:
                if os.path.splitext(filename)[1] == ".mp4" and filename.startswith(
                    category
                ):
                    ff.write("file " + filename + "\n")


# 合并
print(":yum:开始合并")
for root, ds, fs in os.walk(config.get_video_download_path()):
    for filename in fs:
        if os.path.splitext(filename)[1] == ".in":
            #! magic trick
            category = filename[:-3]

            merge_video_files(category)

print(":wine_glass:合并完成")
```



GetVideoIndex.py

```python
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
```



MergeVideoFile.py

```python
import time

from ffmpy3 import FFmpeg
from config.config import Configuration

config = Configuration()


def merge_video_files(category: str):
    """合并视频

    Args:
        in_files (str): 输入视频文件的集合
        category (str): 分类
    """
    ff = FFmpeg(
        global_options=[
            "-loglevel quiet"    
        ],
        inputs={
            config.get_video_download_path()
            + category
            + ".in": "-f concat -safe 0"
        },
        outputs={
            config.get_merged_video_path()
            + category
            + time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(time.time()))
            + ".mp4": None
        }
    )

    ff.run()

```



ParseDownload.py

```python
import time

from ffmpy3 import FFmpeg

from config.config import Configuration
from rich import print

def download_short_video(link, timestamp, author, category) -> bool:
    """下载视频

    Args:
        link (str): 下载地址
        timestamp ([type]): 时间戳
        author ([type]): 作者
        category (str): 所属类别

    Returns:
        bool: 完成
    """
    print(":fire:开始下载")
    # 将 timestamp 转换成 日期
    local = time.localtime(timestamp / 1000.0)
    times = time.strftime("%Y-%m-%d_%H-%M-%S", local)

    path = Configuration().get_video_download_path() + category + "@"

    # 下载的视频写入一个文本 用于合并使用
    # with open(path + 'in.md', 'a') as f:
    #     f.write('file ' + str(times) + author + '.mp4\n')

    ff = FFmpeg(
        inputs={link: None},
        outputs={path + str(times) + author + '.mp4': "-loglevel quiet"})

    ff.run()
    
    return True


```





GraphQLWrapper.py

```python
import requests
from Configuration.PrivateConfig import get_headers

KuaiShouGraphQL = "https://www.kuaishou.com/graphql"
KuaiShouShortVideos = "https://www.kuaishou.com/short-video/"


def get(url, referer=True):
    """向 KuaishouGraphQL 发送 Get 请求

    Args:
        url (str): URL 地址
        referer (bool, optional): 是否添加 Referer 表头. Defaults to True.

    Returns:
        Dict: response.text
    """
    link = KuaiShouShortVideos + url
    if referer:
        diy_head = get_headers(link)
    else:
        diy_head = get_headers("")

    return requests.get(url=link, headers=diy_head, allow_redirects=False).text


def post(js: dict):
    """向 KuaishouGraphQL 发送 POST 请求

    Args:
        js (dict): 封装的请求

    Returns:
        Dict: response.text
    """
    
    response = requests.post(url=KuaiShouGraphQL, json=js, headers=get_headers())
    response.encoding = 'utf-8'
    return response.text


def request_get_home_information(userId: str):
    """个人主页信息

    Args:
        userId (str): 用户 ID

    Returns:
        Dict: 封装的请求
    """
    return {
        "operationName": "visionProfile",
        "query": "query visionProfile($userId: String) {  visionProfile(userId: $userId) {    result    hostName    "
                 "userProfile {      ownerCount {        fan        photo        follow        photo_public        "
                 "__typename      }      profile {        gender        user_name        user_id        headurl       "
                 " user_text        user_profile_bg_url        __typename      }      isFollowing      __typename    "
                 "}    __typename  }} ",
        "variables": {
            "userId": userId
        }
    }


def get_video_real_mp4_path(principle_id: str, photo_id:str):
    """解析视频下载地址

    Args:
        principle_id (str): 作者id
        photo_id (str): 作品id

    Returns:
        Dict: 封装的请求
    """
    return {
        "operationName": "feedById",
        "variables": {
            "principalId": principle_id,
            "photoId": photo_id
        },
        "query": "query feedById($principalId:String, $photoId:String){ currentWorkP{playUrl, poster} }"
    }


def request_get_all_videos(userId: str):
    """获取所有的视频

    Args:
        userId (str): 用户 id

    Returns:
        Dict: 封装的请求 
    """
    return {
        "operationName": "visionProfilePhotoList",
        "variables": {
            "userId": userId,
            "pcursor": "",
            "page": "profile"
        },
        "query": "query visionProfilePhotoList($pcursor: String, $userId: String, $page: String, $webPageArea: "
                 "String) {\n  visionProfilePhotoList(pcursor: $pcursor, userId: $userId, page: $page, webPageArea: "
                 "$webPageArea) {\n    result\n    llsid\n    webPageArea\n    feeds {\n      type\n      author {\n  "
                 "      id\n        name\n        following\n        headerUrl\n        headerUrls {\n          cdn\n "
                 "         url\n          __typename\n        }\n        __typename\n      }\n      tags {\n        "
                 "type\n        name\n        __typename\n      }\n      photo {\n        id\n        duration\n "
                 "  caption\n        likeCount\n        realLikeCount\n        coverUrl\n        coverUrls {\n        "
                 "  cdn\n          url\n          __typename\n        }\n        photoUrls {\n          cdn\n         "
                 " url\n          __typename\n        }\n        photoUrl\n        liked\n        timestamp\n        "
                 "expTag\n        animatedCoverUrl\n        stereoType\n        videoRatio\n        __typename\n      "
                 "}\n      canAddComment\n      currentPcursor\n      llsid\n      status\n      __typename\n    }\n  "
                 "  hostName\n    pcursor\n    __typename\n  }\n}\n "
    }

```





TImestampCalculate.py

```python
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from rich import print
from collections import defaultdict
from icecream import ic
import json
import time

time_unit = {
    "d": 86400000,
    "m": 2678400000
}

def target_timestamp(raw: str) -> int:
    """日期的 raw 格式 返回 timestamp

    Args:
        raw (str): 1d 1m 等

    Returns:
        int: timestamp 对齐至 毫秒
    """
    # 去空格
    name = str(raw).rstrip().lstrip()

    mil_seconds = int(name[:-1]) * time_unit[name[-1]]

    # 对 日期进行数位的对齐 取整
    now = round(time.time() * 1000) 

    return now - mil_seconds



```





config.py

```python
from configparser import ConfigParser


class Configuration:
    """配置信息储存"""

    def __init__(self):
        cfg = ConfigParser()
        cfg.read("./config.ini")
        self.cfg = cfg

    def get_prefix(self) -> str:
        """全局路径前缀

        Returns:
            str: 路径前缀
        """
        return self.cfg.get("Global", "path_prefix")

    def get_merged_video_path(self) -> str:
        """获取合并视频的路径

        Returns:
            str: 合并视频的路径
        """
        return self.get_prefix() + self.cfg.get("Merge", "merged_video")

    def get_video_download_path(self) -> str:
        """获取视频的下载路径

        Returns:
            str: 路径
        """
        return self.get_prefix() + self.cfg.get("Download", "video_download_path")


```

