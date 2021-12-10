import time

from ffmpy3 import FFmpeg
from config.config import Configuration

config = Configuration()

def merge_video_files(category: str):
    """合并视频

    Args:
        in_files (str): 输入视频文件的集合
        category (str): 分类
    """
    ff = FFmpeg(
        inputs={config.get_video_download_path() + category + ".in": "-f concat -safe 0"},
        outputs={
            config.get_merged_video_path()
            + category
            + time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(time.time()))
            + ".mp4": None
        },
    )
    print(ff.cmd)
    
    ff.run()
    

