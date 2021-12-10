from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from rich.pretty import pprint
from rich.progress import Progress
from collections import defaultdict
from icecream import ic
from concurrent.futures import ThreadPoolExecutor
import threading
import json
from utils.TimestampCalculate import target_timestamp
from src.ParseDownload import download_short_video
from src.GetVideoIndex import get_all_videos

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

ic(tasks)

print("请输入你想抓取的视频发布起始日期\n", "格式：13d / 1m")

# 计算目标时间戳
timestamp = target_timestamp(inquirer.text(message="请输入: ").execute())

# 以 类别 为任务单位 分配下载任务
with Progress() as progress:
    for category, _ in tasks.items():

        # ? 任务进度条
        task_progress = progress.add_task("[green]{}".format(category), total=len(_))

        # ? 线程池
        with ThreadPoolExecutor() as pool:
            for one in _:
                # 获取作者的主页视频
                videos = get_all_videos(one["value"][0]["id"], timestamp, one["name"])
                # 此作者的 所有待下载视频个数
                videos_count = len(videos)
                for each_video_k, each_video_v in videos.items():
                    # 提交一个视频的下载
                    task_pool = pool.submit(
                        download_short_video,
                        each_video_v["download"],
                        each_video_v["timestamp"],
                        each_video_v["author"],
                        category,
                    )

                    def push_progress():
                        progress.update(
                            task_progress, advance=1 / videos_count / len(_)
                        )

                    # 推进进度条
                    task_pool.add_done_callback(push_progress)


# 以 类别 位单位 合并每个分类内的视频
