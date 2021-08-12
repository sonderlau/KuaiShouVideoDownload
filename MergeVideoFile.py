import time

from ffmpy3 import FFmpeg
from ParseDownload import path


def merge_video_files():
    ff = FFmpeg(
        inputs={path + 'in.md': "-f concat -safe 0"},
        outputs={path + time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(time.time())) + '.mp4': None})
    print(ff.cmd)
    ff.run()

