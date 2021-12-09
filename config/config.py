from configparser import ConfigParser


class Configuration:
    """配置信息储存"""

    def __init__(self):
        cfg = ConfigParser()
        cfg.read("./config.ini")
        self.cfg = cfg

    def get_prefix(self) -> str:
        """全局路径前缀

        Returns:
            str: 路径前缀
        """
        return self.cfg.get("Global", "path_prefix")

    def get_merged_video_path(self) -> str:
        """获取合并视频的路径

        Returns:
            str: 合并视频的路径
        """
        return self.get_prefix() + self.cfg.get("Merge", "merged_video")

    def get_video_download_path(self) -> str:
        """获取视频的下载路径

        Returns:
            str: 路径
        """
        return self.get_prefix() + self.cfg.get("Download", "video_download_path")

