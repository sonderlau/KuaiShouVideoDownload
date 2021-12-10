from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from rich.pretty import pprint
from collections import defaultdict
from icecream import ic
import json
from utils.TimestampCalculate import target_timestamp

# 整理
tasks = defaultdict(lambda: [])

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

print("请输入你想抓取的视频发布起始日期\n", "格式：13d / 1m")
name = inquirer.text(message="请输入: ").execute()

# 计算目标时间戳
timestamp = target_timestamp(name)
