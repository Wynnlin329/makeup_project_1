# !/usr/bin/python
# vim: set fileencoding:utf-8
#-*- coding: cp950 -*-
#-*- coding: utf-8 -*-

import os
import re
import sys
import json
import time
import random
import requests
from hashlib import md5
from pyquery import PyQuery as pq

url_base = 'https://www.instagram.com/'
uri = 'https://www.instagram.com/graphql/query/?query_hash=a5164aed103f24b03e7b7747a2d94e3c&variables=%7B%22id%22%3A%22{user_id}%22%2C%22first%22%3A12%2C%22after%22%3A%22{cursor}%22%7D'


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
    'cookie': 'csrftoken=Cl6VG5EiUw8leEXpTTbBp3eKawVcIMcG; mid=XVpTjwALAAGmDIh95C7neIRgSA4z; rur=ATN'}


def get_html(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print('請求網頁源代碼錯誤, 錯誤狀態碼：', response.status_code)
    except Exception as e:
        print(e)
        return None


def get_json(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print('請求網頁json錯誤, 錯誤狀態碼：', response.status_code)
    except Exception as e:
        print(e)
        time.sleep(60 + float(random.randint(1, 4000))/100)
        return get_json(url)


def get_content(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.content
        else:
            print('請求照片二進制流錯誤, 錯誤狀態碼：', response.status_code)
    except Exception as e:
        print(e)
        return None


def get_urls(html):
    urls = []
    user_id = re.findall('"profilePage_([0-9]+)"', html, re.S)[0]
    print('user_id：' + user_id)
    doc = pq(html)
    items = doc('script[type="text/javascript"]').items()
    for item in items:
        if item.text().strip().startswith('window._sharedData'):
            js_data = json.loads(item.text()[21:-1], encoding='utf-8')
            edges = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]
            page_info = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]['page_info']
            cursor = page_info['end_cursor']
            flag = page_info['has_next_page']
            for edge in edges:
                if edge['node']['display_url']:
                    display_url = edge['node']['display_url']
                    print(display_url)
                    urls.append(display_url)
            print(cursor, flag)
    while flag:
        url = uri.format(user_id=user_id, cursor=cursor)
        js_data = get_json(url)
        infos = js_data['data']['user']['edge_owner_to_timeline_media']['edges']
        cursor = js_data['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
        flag = js_data['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
        for info in infos:
            if info['node']['is_video']:
                video_url = info['node']['video_url']
                if video_url:
                    print(video_url)
                    urls.append(video_url)
            else:
                if info['node']['display_url']:
                    display_url = info['node']['display_url']
                    print(display_url)
                    urls.append(display_url)
        print(cursor, flag)
        # time.sleep(4 + float(random.randint(1, 800))/200)    # if count > 2000, turn on
    return urls


def main(user):
    url = url_base + user + '/'
    html = get_html(url)
    urls = get_urls(html)
    dirpath = r'c:/{0}'.format(user)
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    for i in range(len(urls)):
        print('\n正在下載第{0}張： '.format(i) + urls[i], ' 還剩{0}張'.format(len(urls)-i-1))
        try:
            content = get_content(urls[i])
            file_path = r'c:/{0}/{1}.{2}'.format(user, md5(content).hexdigest(), urls[i][-43:-40])
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    print('第{0}張下載完成： '.format(i) + urls[i])
                    f.write(content)
                    f.close()
            else:
                print('第{0}張照片已下載'.format(i))
        except Exception as e:
            print(e)
            print('這張圖片or視頻下載失敗')


if __name__ == '__main__':
    user_name = sys.argv[1]
    start = time.time()
    main(user_name)
    print('Complete!!!!!!!!!!')
    end = time.time()
    spend = end - start
    hour = spend // 3600
    minu = (spend - 3600 * hour) // 60
    sec = spend - 3600 * hour - 60 * minu
    print(f'一共花費了{hour}小時{minu}分鐘{sec}秒')
    
