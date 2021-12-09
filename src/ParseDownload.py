import time

from ffmpy3 import FFmpeg

from Configuration.config import Configuration


def download_short_video(link, timestamp, author):

    # 将 timestamp 转换成 日期
    local = time.localtime(timestamp / 1000.0)
    times = time.strftime("%Y-%m-%d_%H-%M-%S", local)

    path = Configuration().get_video_download_path()

    # 下载的视频写入一个文本 用于合并使用
    with open(path + 'in.md', 'a') as f:
        f.write('file ' + str(times) + author + '.mp4\n')

    ff = FFmpeg(
        inputs={link: None},
        outputs={path + str(times) + author + '.mp4': None})

    ff.run()

