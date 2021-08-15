# KuaiShouVideoDownload

起因是我自己喜欢看快手上的快餐视频，但我不想打开快手的客户端。
上面的推广和各种广告会很浪费精力。

于是我用简单的 `Python` 编写了一个自动下载视频并合并成一个的脚本
## 引用库
- `FFmpy3` `FFmpeg`
  - 请务必在你的运行环境中安装这两者

## 文件介绍

- `Test` 目录
  - 其中有两个 python文件是我用于测试某些功能能否按照预期运行的
  - `ApiDemo` 中 是我抓包时获取的返回样例，如果你想自定义修改部分内容或者添加新功能，请参考
- `Configuration` 目录
  - `config.py` 获取相关配置路径
  - `GraphQLWrapper.py` 对网络获取请求进行了简单的封装
  - `PrivateConfig.py` **注意！请手动添加并修改此文件** 
- `GetVideoIndex.py` 获取某人的所有主页视频，生成`dict` 其包含
  - 视频`id`
  - 发布时间`timestamp`
  - 作者名称 `author`
- `ParseDownload.py` 将视频的网页地址解析，并下载视频为`mp4`文件
- `MergeVideoFile.py` 将下载下来的多个视频合并成一个
- `last_update.md` 记录最后一次获取视频的时间戳
  - 请勿手动修改 除非你知道自己在做什么
- `run.py` 启动文件 运行该文件即可

## 特点

- 根据视频发布的时间进行排序
- 方便加入新的视频主

## 使用
如果打算使用，请严格遵循以下步骤

- 确认运行环境已经安装好 `Python` `FFmpeg` `FFmpy3`
- 使用当前的网络环境通过浏览器，登录并访问快手PC版一次，并在 浏览器的`Network`中获取所需要的 Header

- 在 `Configuration` 文件夹下添加`PrivateConfig.py` 文件，并将`Header` 添加进去，其形式应该类似于如下的样例

  - ```python
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
        "Cookie": "kpf=PC_WEB; "
                  "kpn=KUAISHOU_VISION; "
                  "clientid=3; "
                  "did=web_4e01exxxx; "
                  "client_key=658xxxx; "
                  "userId=188xxxxxxx; "
                  "kuaishou.server.web_st=ChZrdWFpc2hvdS5zZXJ2ZXIud2ViLnN0EqABlmfs6GfuoGejIqbhpihfBye2pKR6hx5f4oSAlsosDPkaIOCE6UvVXgype610JYkZVr8k7ZXsYkuWEDnXmVj7-LXVGYLavMhi4zMsr4fXAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx; "
                  "kuaishou.server.web_ph=3340eeff74640xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    }
    ```

- 修改 `config.ini` 中的路径，使用你自己的路径
  - 由于我使用的是 `WSL2 Ubuntu` 请记得修改成相应操作系统的路径格式

## TODO
- [ ] 可以生成多个视频 方便做更多的集合
- [ ] 下载视频部分使用多线程或者异步完成
- [x] 配置文件分离
- [ ] 修改参数 提高视频画质