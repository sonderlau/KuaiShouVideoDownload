import requests
from Configuration.PrivateConfig import get_headers

KuaiShouGraphQL = "https://www.kuaishou.com/graphql"
KuaiShouShortVideos = "https://www.kuaishou.com/short-video/"


def get(url, referer=True):
    link = KuaiShouShortVideos + url
    if referer:
        diy_head = get_headers(link)
    else:
        diy_head = get_headers("")

    return requests.get(url=link, headers=diy_head, allow_redirects=False).text


def post(js):
    response = requests.post(url=KuaiShouGraphQL, json=js, headers=get_headers())
    response.encoding = 'utf-8'
    return response.text


def request_get_home_information(userId: str):
    """个人主页信息

    Args:
        userId (str): 用户 ID

    Returns:
        Dict: 封装的请求
    """
    return {
        "operationName": "visionProfile",
        "query": "query visionProfile($userId: String) {  visionProfile(userId: $userId) {    result    hostName    "
                 "userProfile {      ownerCount {        fan        photo        follow        photo_public        "
                 "__typename      }      profile {        gender        user_name        user_id        headurl       "
                 " user_text        user_profile_bg_url        __typename      }      isFollowing      __typename    "
                 "}    __typename  }} ",
        "variables": {
            "userId": userId
        }
    }


def get_video_real_mp4_path(principle_id: str, photo_id:str):
    """解析视频下载地址

    Args:
        principle_id (str): 作者id
        photo_id (str): 作品id

    Returns:
        Dict: 封装的请求
    """
    return {
        "operationName": "feedById",
        "variables": {
            "principalId": principle_id,
            "photoId": photo_id
        },
        "query": "query feedById($principalId:String, $photoId:String){ currentWorkP{playUrl, poster} }"
    }


def request_get_all_videos(userId: str):
    """获取所有的视频

    Args:
        userId (str): 用户 id

    Returns:
        Dict: 封装的请求 
    """
    return {
        "operationName": "visionProfilePhotoList",
        "variables": {
            "userId": userId,
            "pcursor": "",
            "page": "profile"
        },
        "query": "query visionProfilePhotoList($pcursor: String, $userId: String, $page: String, $webPageArea: "
                 "String) {\n  visionProfilePhotoList(pcursor: $pcursor, userId: $userId, page: $page, webPageArea: "
                 "$webPageArea) {\n    result\n    llsid\n    webPageArea\n    feeds {\n      type\n      author {\n  "
                 "      id\n        name\n        following\n        headerUrl\n        headerUrls {\n          cdn\n "
                 "         url\n          __typename\n        }\n        __typename\n      }\n      tags {\n        "
                 "type\n        name\n        __typename\n      }\n      photo {\n        id\n        duration\n "
                 "  caption\n        likeCount\n        realLikeCount\n        coverUrl\n        coverUrls {\n        "
                 "  cdn\n          url\n          __typename\n        }\n        photoUrls {\n          cdn\n         "
                 " url\n          __typename\n        }\n        photoUrl\n        liked\n        timestamp\n        "
                 "expTag\n        animatedCoverUrl\n        stereoType\n        videoRatio\n        __typename\n      "
                 "}\n      canAddComment\n      currentPcursor\n      llsid\n      status\n      __typename\n    }\n  "
                 "  hostName\n    pcursor\n    __typename\n  }\n}\n "
    }
