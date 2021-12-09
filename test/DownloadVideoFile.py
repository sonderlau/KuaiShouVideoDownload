import ffmpy3

ff = ffmpy3.FFmpeg

ffmpy3.FFmpeg(
    inputs={'http://youku.com-youku.net/20180614/11920_4c9e1cc1/index.m3u8': None},
    outputs={'第001集.mp4': [
        '-maxrate 6000k'
    ]}) \
    .run()
