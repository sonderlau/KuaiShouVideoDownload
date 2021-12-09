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

# 指定下载的时间
print("请输入你想抓取的视频发布起始日期\n", "格式：13d / 1m")
name = inquirer.text(message="请输入: ").execute()

# 去空格
name = str(name).rstrip().lstrip()

mil_seconds = int(name[:-2]) * time_unit[name[-1]]

# 对 日期进行数位的对齐 取整
now = round(time.time() * 1000) 

target_timestamp = now - mil_seconds

