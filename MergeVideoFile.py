import time

from ffmpy3 import FFmpeg
from Configuration.config import Configuration


def merge_video_files():
    path = Configuration().get_merged_video_path()
    ff = FFmpeg(
        inputs={path + 'in.md': "-f concat -safe 0"},
        outputs={path + time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(time.time())) + '.mp4': None})
    print(ff.cmd)
    ff.run()

