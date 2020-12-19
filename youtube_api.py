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
index = 0

youtube = build(
    YOUTUBE_API_SERVICE_NAME,
    YOUTUBE_API_VERSION,
    developerKey = APY_KEY
)


def getChannel():
    global index
    response = youtube.search().list(q=SEARCH_TEXT, part='id,snippet', maxResults=10).execute()

    for item in response.get('items', []):
        if item['id']['kind'] != 'youtube#channel':
            continue
        channel_dict = {'index':str(index),'title':item['snippet']['title'],'channelId':item['snippet']['channelId']}
        channel_list.append(channel_dict)
        index += 1
    print(channel_list)

getChannel()
