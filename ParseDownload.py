import time

from ffmpy3 import FFmpeg
import requests
import re

path = '/mnt/d/download/'


def download_short_video(link, timestamp, author):
    link = "https://www.kuaishou.com/short-video/" + link

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Mobile Safari/537.36",
        "Referer": link,
        "Cookie": "kpf=PC_WEB; kpn=KUAISHOU_VISION; clientid=3; did=web_4e01e3c76fca2709eaad05b36b30db0a; client_key=65890b29; userId=1884279497; kuaishou.server.web_st=ChZrdWFpc2hvdS5zZXJ2ZXIud2ViLnN0EqABlmfs6GfuoGejIqbhpihfBye2pKR6hx5f4oSAlsosDPkaIOCE6UvVXgype610JYkZVr8k7ZXsYkuWEDnXmVj7-LXVGYLavMhi4zMsr4fXAuv4oJHxVN1qjDGH9bgSX-k4DqzZ2xc9uNulZ8QIZ0SFgqAepdhrh0qjvVBwYjnEkCxcNl6mhJSR0ae4bv2J0VZKXer1kP1m72RrK9y4PUHlsRoSWXnZQFypWC8Fi7687FtZGgfDIiDYnEE5pCSMbI7VNuFrXnrShn0zLQw5hxXHa5STt1iTRigFMAE; kuaishou.server.web_ph=3340eeff746400da08533ae710bafdaff38a"
    }

    json_data = requests.get(url=link, headers=headers, allow_redirects=True).text
    res = re.findall('type="video/mp4" src="(.*?)"', json_data)[0]

    # 将 timestamp 转换成 日期
    local = time.localtime(timestamp / 1000.0)
    times = time.strftime("%Y-%m-%d_%H-%M-%S", local)

    with open(path + 'in.md', 'a') as f:
        f.write('file ' + str(times) + author + '.mp4\n')

    ff = FFmpeg(
        inputs={res: None},
        outputs={path + str(times) + author + '.mp4': None})

    ff.run()




# if __name__ == '__main__':
#     download_short_video('3xdg9js6qn3u9ii', 1628675403899, '成杰')
