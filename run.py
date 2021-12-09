import time
from typing import List

from GetVideoIndex import get_all_videos
from MergeVideoFile import merge_video_files
from ParseDownload import download_short_video
from config.config import Configuration
from rich.console import Console


def run(category: str, names: List, last_update: str):
    """运行视频下载

    Args:
        category (str): 类别
        names (List): 当前分类下的人
    """

    result = {}

    # 遍历所有的人 查找符合条件的视频
    for key in names:
        result.update(
            get_all_videos(user_id=key, last_update=last_update, author_name=key)
        )

    # 对所有的作品进行时间的排序
    sorted(result, key=lambda x: result[x]["timestamp"])

    # 输入文件清空
    with open(Configuration().get_video_download_path() + "in.md", "w") as fl:
        fl.write("")
    # 对所有作品进行下载
    for key in result:
        download_short_video(
            result[key]["download"], result[key]["timestamp"], result[key]["author"]
        )

    # 合并视频
    merge_video_files()

    # 写入最后一次更新的时间
    with open("./last_update_md", "w") as flush:
        flush.write(
            str(int(time.time() * 1000.0))
            + "\n\n"
            + time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(time.time()))
        )
