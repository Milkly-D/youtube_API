#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from apiclient.discovery import build

APY_KEY = '<your API key>'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
SEARCH_TEXT ='<search word>'

channel_list = []
video_list = []
num = 0

youtube = build(
    YOUTUBE_API_SERVICE_NAME,
    YOUTUBE_API_VERSION,
    developerKey = APY_KEY
)

def getChannelId(_num,_items):
    for data in _items:
        if data['num'] == _num:
            return data['channelId']
    return ''

def getChannel():
    global num
    response = youtube.search().list(q=SEARCH_TEXT, part='id,snippet', maxResults=10,type='channel').execute()

    for item in response.get('items', []):
        if item['id']['kind'] != 'youtube#channel':
            continue
        num += 1
        channel_dict = {'num':str(num),'title':item['snippet']['title'],'channelId':item['snippet']['channelId']}
        channel_list.append(channel_dict)
    
    print('***Channel list***')
    for data in channel_list:
        print("Channel " + data["num"] + " : " + data["title"])
    print('******************')

<<<<<<< HEAD

getChannel()
print(getChannelId(str(input('Channel Number: ')),channel_list))
=======
getChannel()
>>>>>>> origin/master
