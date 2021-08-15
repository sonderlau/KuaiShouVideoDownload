from PrivateConfig import headers
import requests

KuaiShouGraphQL = "https://www.kuaishou.com/graphql"
KuaiShouShortVideos = "https://www.kuaishou.com/short-video/"


def get(link, Referer=True):
    link = KuaiShouShortVideos + link

    return requests.get(url=link, headers=get_headers(link if Referer else ""), allow_redirects=True).text


def post(js):
    response = requests.post(url=KuaiShouGraphQL, json=js, headers=get_headers())
    response.encoding = 'utf-8'
    return response.text


def get_headers( link=""):
    if link == "":
        return headers
    else:
        h = headers['Referer'] = link
        return h


def request_get_home_infomation(userId):
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


def request_get_all_videos(userId):
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
