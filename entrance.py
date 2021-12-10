import json
import os
from collections import defaultdict
from concurrent.futures import ALL_COMPLETED, ThreadPoolExecutor, wait

from icecream import ic
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from rich.pretty import pprint
from rich.progress import Progress

from src.GetVideoIndex import get_all_videos
from src.ParseDownload import download_short_video
from src.MergeVideoFile import merge_video_files
from utils.TimestampCalculate import target_timestamp
from config.config import Configuration

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
        transformer=lambda result: "%s region%s selected"
        % (len(result), "s" if len(result) > 1 else ""),
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

pprint(tasks)

print("请输入你想抓取的视频发布起始日期\n", "格式：13d / 1m")

# 计算目标时间戳
timestamp = target_timestamp(inquirer.text(message="请输入: ").execute())

# 以 类别 为任务单位 分配下载任务

for category, _ in tasks.items():

    # ? 线程池
    with ThreadPoolExecutor() as pool:
        thread_pool_list = []
        for one in _:
            # 获取作者的主页视频
            pprint([one["value"][0]["id"], timestamp, one["name"]])
            videos = get_all_videos(one["value"][0]["id"], timestamp, one["name"])
            pprint(videos)
            # 此作者的 所有待下载视频个数
            for each_video_k, each_video_v in videos.items():
                # 提交一个视频的下载
                task_pool = pool.submit(
                    download_short_video,
                    each_video_v["download"],
                    each_video_v["timestamp"],
                    each_video_v["author"],
                    category,
                )

                thread_pool_list.append(task_pool)

        wait(thread_pool_list, return_when=ALL_COMPLETED)

        # 以 类别 位单位 合并每个分类内的视频
    with open(
        config.get_video_download_path() + category + ".in",
        mode="w",
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
pprint("开始合并")
for root, ds, fs in os.walk(config.get_video_download_path()):
    for filename in fs:
        if os.path.splitext(filename)[1] == ".in":
            #! magic trick
            category = filename[:-3]

            merge_video_files(category)
