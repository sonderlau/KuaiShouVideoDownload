# Kuai Shou Video Downloader

:warning: This programme is not on stable version, please do not use in production enviroment.

---


I love to watch some types of videos on Kuaishou
However, this app has a lot of ADs and unnessary recommendations which distract my attention from time to time.

So I write this project in `Python`, so it can automatically download the videos that I specified
and merge those in the same category to a single video file.

## Requirements

- `FFmpy3` `FFmpeg`
  - for FFmpeg, you can download it from the [offical website](https://ffmpeg.org/)
  - for FFmpy3, run `pip install -r requirements.txt`, or install this package manually.

## Project Structure

- `Test` Codes to test some functions.
- `API` I captured some requests on the Kuaishou Webpage, to analyse the format of datas.
- `Configuration` 
  - `PrivateConfig.py` **WARNING！Please create this file manually and file in your personal information** 
- `GetVideoIndex.py` List someone's whole uploaded videos，generate a `dict`  for return.
  - VideoId `id`
  - UploadedTime`timestamp`
  - Author's name `author`
- `ParseDownload.py` Parse the HTML file to download videos in `mp4` format.
- `MergeVideoFile.py` Merge videos into a single file.
- `last_update.md` log the last update time.
  - Please do not edit it, unless you know exactly what you are doing.
- `run.py` The entrance, just run this file and you are good to go.

## Features

- Sort videos by its uploaded time.
- Easily add new authors.

## Usage

Please follow these steps to run:

- Make sure you have installed `Python` `FFmpeg` `FFmpy3`
- Visit Kuaishou PC webpage at least once, and open the browser's DevTools, usually press F12.
- Checkout in the DevTools/Network tab, and collect `Header` infos.

- In `Configuration` directory, create`PrivateConfig.py` file，put your `Header` informations in it，the `Header` should be look like this:

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

- Edit `config.ini`, you can set the video path in here.
  - I'm using `WSL2 Ubuntu` for development, if you are using Windows, please change it to Windows format.

## TODO
- [ ] Generate more type of videos
- [ ] Async or multi-threads
- [x] Separate the config file
- [ ] Improve video quality
- [ ] Use `Rich` package for more humanistic tips.
