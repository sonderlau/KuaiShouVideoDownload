import time

from ffmpy3 import FFmpeg
from Configuration.config import Configuration


def merge_video_files():
    path = Configuration().get_merged_video_path()
    in_path = Configuration().get_video_download_path()
    ff = FFmpeg(
        inputs={in_path+ 'in.md': "-f concat -safe 0"},
        outputs={path + time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(time.time())) + '.mp4': None})
    print(ff.cmd)
    ff.run_async()
    await ff.wait()


if __name__ == '__main__':
    merge_video_files()