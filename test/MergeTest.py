import os
from src.MergeVideoFile import merge_video_files
from config.config import Configuration
config = Configuration()


# 合并
print("开始合并")
for root, ds, fs in os.walk(config.get_video_download_path()):
    for filename in fs:
        if os.path.splitext(filename)[1] == ".in":
            #! magic trick
            category = filename[:-3]

            merge_video_files(category)