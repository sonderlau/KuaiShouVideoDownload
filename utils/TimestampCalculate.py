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
    # 去空格
    name = str(raw).rstrip().lstrip()

    mil_seconds = int(name[:-1]) * time_unit[name[-1]]

    # 对 日期进行数位的对齐 取整
    now = round(time.time() * 1000) 

    return now - mil_seconds


