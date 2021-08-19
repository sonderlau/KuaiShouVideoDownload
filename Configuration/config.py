from configparser import ConfigParser


class Configuration:
    def __init__(self):
        cfg = ConfigParser()
        cfg.read("./config.ini")
        self.cfg = cfg

    def get_prefix(self):
        return self.cfg.get('Global', 'path_prefix')

    def get_merged_video_path(self):
        return self.get_prefix() + self.cfg.get('Merge', 'merged_video')

    def get_video_download_path(self):
        return self.get_prefix() + self.cfg.get('Download', 'video_download_path')


if __name__ == '__main__':
    print(Configuration().get_video_download_path())
