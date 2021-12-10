import subprocess

from config.config import Configuration
from ffmpy3 import FFmpeg

config = Configuration()

prefix = "/mnt/d/repositories/KuaiShouVideoDownload/out/"

cmd = [
    "ffmpeg -f concat -safe 0 -i "
    + config.get_merged_video_path()
    + "in"
    + config.get_merged_video_path()
    + "merged.mp4"
    + " -hide_banner"
]

process = subprocess.Popen(
    cmd,
    shell=True,
    stdout=subprocess.STDOUT,
    stderr=subprocess.STDOUT,
    encoding="utf-8",
    text=True,
)

# frame=   74 fps= 41 q=29.0 size=     256kB time=00:00:02.79 bitrate= 749.5kbits/s speed=1.55x
for line in process.stdout:
    print(line)
