import time

from GetVideoIndex import get_all_videos
from MergeVideoFile import merge_video_files
from ParseDownload import download_short_video, path

index = {
    '3x4g2b9attf6q9u': "成杰",

    '3xm4ygx7iisxj5e': "老头",

    '3xfjfdnmb78vh3m': "浪人",

    '3xwaxvfvcps7awu': "小石",

    '3xxd79tgpnd5tqy': "多多",

    '3xvsnr6zrmvzijc': "浪言",

    '3xfeqrftsqvbisu': "表弟",

    '3xhu9p77zphvbbs': "大表弟",

    '3x2k7pdreevzzn6': "扛把子"
}

if __name__ == '__main__':

    # 读取上一次更新的时间
    with open('./last_update.md', 'r') as f:
        last_update = f.readlines()[0]
        result = {}

        # 遍历所有的人 查找符合条件的视频
        for key in index:
            result.update(get_all_videos(key, last_update, index[key]))

        # 对所有的作品进行时间的排序
        sorted(result, key=lambda x: result[x]['timestamp'])
        print(result)

        # 输入文件清空
        with open(path + 'in.md', 'w') as fl:
            fl.write('')

        # 对所有作品进行下载
        for key in result:
            download_short_video(key, result[key]['timestamp'], result[key]['author'])

        # 合并视频
        merge_video_files()

        # 写入最后一次更新的时间
        with open('./last_update_md', 'w') as flush:
            flush.write(
                str(int(time.time() * 1000.0)) + '\n\n' + time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(time.time())))
