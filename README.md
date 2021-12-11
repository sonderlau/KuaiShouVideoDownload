# Kuai Shou Video Downloader

Release: V1.1

---

起因是我自己喜欢看快手上的快餐视频，但我不想打开快手的客户端。
上面的推广和各种广告会很浪费精力。

于是我用简单的 `Python` 编写了一个自动下载视频并合并成一个的脚本

## 引用库

-  `FFmpeg`
- 安装 Python 所需库

```python
pip install -r requirements.txt
```

## 文件介绍

- `Test` 目录
  - 均为用来测试部分代码所用的
  - 有部分代码未真正使用
- `config` 目录
  - `config.py` 配置文件获取的包装
  - `subscription.json` 选项的保存
- `src` 目录
  - `GetVideoIndex.py` 获取某人的所有主页视频，生成`dict`
  - `ParseDownload.py` 将视频的网页地址解析，并下载视频为`mp4`文件
  - `MergeVideoFile.py` 将下载下来的多个视频合并成一个
- `config.ini` 下载的地址配置
  - 请修改
- `entrance.py` 启动文件 运行该文件即可

## 特点

- 根据视频发布的时间进行排序
- 根据指定的时间进行范围内选取
- 按类别进行抓取并合并
- 使用线程池对下载进行加速

## 使用

如果打算使用，请严格遵循以下步骤

- 确认运行环境已经安装好 `Python` `FFmpeg` 并安装所需要的 Python 环境库
- 使用当前的网络环境通过浏览器，登录并访问快手 PC 版一次，并在 浏览器的`Network`中找到向 `www.kuaishou.com/graphql` 地址发送的请求，并查看该请求中的 Header 中的 Cookie 部分
- 在 `Configuration` 文件夹下添加或修改`PrivateConfig.py` 文件，并将`Header` 添加进去，其形式应该类似于如下的样例

  -

````python
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
  + 由于我使用的是 `WSL2 Ubuntu` 请记得修改成相应操作系统的路径格式

## TODO

* [x] 可以生成多个视频 方便做更多的集合
* [x] 下载视频部分使用多线程或者异步完成
* [x] 配置文件分离
* [ ] 修改参数 提高视频画质
* [ ] 使用`Rich` 提供更人性化的进度展示
* [x] 指定最后截取的日期
* [x] 多线程下载视频
* [x] 选择的人进行储存
````
