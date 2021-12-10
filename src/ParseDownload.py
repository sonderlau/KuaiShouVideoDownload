import time

from ffmpy3 import FFmpeg

from config.config import Configuration


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

    # 将 timestamp 转换成 日期
    local = time.localtime(timestamp / 1000.0)
    times = time.strftime("%Y-%m-%d_%H-%M-%S", local)

    path = Configuration().get_video_download_path() + category

    # 下载的视频写入一个文本 用于合并使用
    with open(path + 'in.md', 'a') as f:
        f.write('file ' + str(times) + author + '.mp4\n')

    ff = FFmpeg(
        inputs={link: None},
        outputs={path + str(times) + author + '.mp4': None})

    ff.run()
    
    return True

