from PyInquirer import prompt, Separator

from examples import custom_style_2
from icecream import ic
import json

with open("./config/subscription.json", "r") as fp:
    questions = json.load(fp)

    pre_set = [
        {
            "type": "checkbox",
            "qmark": "😃",
            "message": "选择要下载的视频",
            "name": "Kuaishou Download",
            "choices": [],
            "validate": lambda answer: "请至少选择一个视频" if len(answer) == 0 else True,
        }
    ]

    choices = pre_set[0]["choices"]

    # json 文件内容解析
    for k, v in questions.items():
        choices.append(Separator("= {} =".format(k)))

        cnt = 0
        for dv in v:
            choices.append(
                {
                    "name": dv["name"],
                    "value": [
                        dv["value"],
                        
                        # ? 所属分类
                        k,   
                        
                        # ? 所在位置
                        cnt
                    ],
                    "checked": dv["checked"]
                }
            )
            cnt += 1

    pre_set[0]["choices"] = choices
    answers = prompt(pre_set, style=custom_style_2)

    ic(answers)

    # 对选择内容写入文件

    for _ in answers.values():
        for i in _:
            questions[i[1]][i[2]]["checked"] = True
    
    ic(questions)
    
    with open('./config/subscription.json', 'w') as fp:
        json.dump(questions, fp)
