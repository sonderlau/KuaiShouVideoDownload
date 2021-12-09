import time

from ffmpy3 import FFmpeg


def merge_video_files(in_files: str, category: str) -> bool:
    """合并视频

    Args:
        in_files (str): 输入视频文件的集合
        category (str): 分类

    Returns:
        bool: 是否完成
    """
    ff = FFmpeg(
        inputs={in_path + "in.md": "-f concat -safe 0"},
        outputs={
            path
            + time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(time.time()))
            + ".mp4": None
        },
    )
    print(ff.cmd)
    
    ff.run_async()
    
    return True

