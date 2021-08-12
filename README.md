# KuaiShouVideoDownload

起因是我自己喜欢看快手上的快餐视频，但我不想打开快手的客户端。
上面的推广和各种广告会很浪费精力。

于是我用简单的`Python` 编写了一个自动下载视频并合并成一个的脚本
## 引用库
- `FFmpy3` `FFmpeg`

## 文件介绍

- `GetVideoIndex.py` 获取某人的所有主页视频，生成`dict` 其包含
  - 视频`id`
  - 发布时间`timestamp`
  - 作者名称 `author`
- `ParseDownload.py` 将视频的网页地址解析，并下载视频为`mp4`文件
- `MergeVideoFile.py` 将下载下来的多个视频合并成一个
- `last_update.md` 记录最后一次获取视频的时间戳
- `run.py` 启动文件 运行该文件即可

## 特点

- 根据视频发布的时间进行排序
- 方便加入新的视频主

## 配置
如果你自己使用，请注意修改以下几点
- `GetVideoIndex.py` `ParseDownload.py` 两个文件中关于 `headers` 部分
  - 你需要修改成你当前使用端 访问网页版快手 抓包 `GraphQL`中你自己的 cookies
- 修改 `ParseDownload.py` 中 `path` 部分
  - 由于我使用的是 `WSL2 Ubuntu` 请记得修改成你自己的下载地址

## TODO
- 可以生成多个视频 方便做更多的集合
- 下载视频部分使用多线程或者异步完成
- 配置文件分离
- 修改参数 提高视频画质