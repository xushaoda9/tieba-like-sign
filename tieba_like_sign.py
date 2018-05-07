# -*- coding:utf-8 -*-

__author = 'shaoda.xu'

import urllib
import requests

headers = {
    "Host": "passport.baidu.com",
    "Referer": "https://www.baidu.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36"
}

cookies = {
    'BDUSS': 'h0cDQ2Mmd0SnZHQVpZTlZVWSUthQ0dteUxJWFhXb2tadn5rZzN2Y2RaSVFBQUFBJCQAAAAAAAAAAAEAAABne-WeRMLtzOMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADcwoFk3MKBZQW'}


# 获得贴吧ID: fid
def get_fid(tieba_name):
    fid_url = "http://tieba.baidu.com/f/commit/share/fnameShareApi?ie=utf-8&fname=" + tieba_name
    response = requests.get(fid_url)
    response_data = response.json()
    return response_data['data']['fid']


def get_tbs():
    url_tbs = 'http://tieba.baidu.com/dc/common/tbs'
    return requests.get(url_tbs, cookies=cookies, headers=headers).json()['tbs']


# 贴吧签到
def tieba_sign(tieba_name):
    like_url = "https://tieba.baidu.com/sign/add"
    headers["Host"] = "tieba.baidu.com"

    tbs = get_tbs()
    print(tbs)

    like_data = {
        'ie': "utf-8",  # gbk
        'kw': tieba_name,  # 贴吧名称
        'tbs': tbs  # 获取tbs
    }

    response_data = requests.post(like_url, data=like_data, cookies=cookies, headers=headers)
    response_data.encoding = "utf-8"
    # print(response_data.text)
    response_json = response_data.json()
    if response_json['no'] == 1101:
        print("signed before")
    elif response_json['no'] == 0:
        print("sign completed")
    else:
        print("sign error")


# 贴吧关注
def tieba_like(tieba_name, uid):
    like_url = "https://tieba.baidu.com/mo/q/favolike"
    headers["Host"] = "tieba.baidu.com"

    fid = get_fid(tieba_name)
    url_tbs = 'http://tieba.baidu.com/dc/common/tbs'
    tbs = requests.get(url_tbs, cookies=cookies).json()['tbs']

    like_data = {
        'uid': uid,  # 贴吧帐号
        'fid': fid,  # 贴吧fid
        'kw': tieba_name,  # gbk
        'itb_tbs': tbs,  # 获取tbs
    }
    like_data = urllib.parse.urlencode(like_data)
    like_url = like_url + "?" + like_data

    response_data = requests.get(like_url, cookies=cookies)
    print(response_data.text)


if __name__ == "__main__":
    uid = "2669463"
    tieba_like("死神", uid)
    tieba_sign("死神")
