#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
import pandas as pd
from apiclient.discovery import build

URL = 'https://www.googleapis.com/youtube/v3/'
API_KEY = '<API_KEY>'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
SEARCH_QUELY =''

youtube = build(
    YOUTUBE_API_SERVICE_NAME,
    YOUTUBE_API_VERSION,
    developerKey = API_KEY
)

def run():
    global SEARCH_QUELY
    SEARCH_QUELY = input('検索ワード>> ')
    dataList(getComments(getVideos(getChannel())))

def getId(_num,_items):
    for data in _items:
        if data['num'] == _num:
            if data['type'] == 'youtube#channel':
                return data['channelId']
            else:
                return data['videoId']
    return ''

def getChannel():
    channel_list = []
    num = 0
    search_res = youtube.search().list(
        q=SEARCH_QUELY, 
        part='id,snippet', 
        maxResults=10,
        type='channel',
        order='rating'
    ).execute()

    for item in search_res.get('items', []):
        num += 1
        channel_dict = {'num':str(num),'type':item['id']['kind'],'title':item['snippet']['title'],'channelId':item['snippet']['channelId']}
        channel_list.append(channel_dict)
    
    print('***Channel list***')
    for data in channel_list:
        print("Channel " + data["num"] + " : " + data["title"])
    print('******************')

    return getId(input('Channel Number>> '),channel_list)

def getVideos(_channelId):
    video_list = []
    num = 0
    video_res = youtube.search().list(
        part = 'snippet',
        channelId = _channelId,
        maxResults = 100,
        type = 'video',
        order = 'date'
    ).execute()
    
    for item in video_res.get("items",[]):
        num += 1
        video_dict = {'num':str(num),'type':item['id']['kind'],'title':item['snippet']['title'],'videoId':item['id']['videoId']}
        video_list.append(video_dict)

    print('***Video list***')
    for data in video_list:
        print("Video " + data["num"] + " : " + data["title"])
    print('****************')

    return getId(input('Video Number>> '),video_list)

def getComments(_videoId):
    global API_KEY
    comment_list = []
    params = {
        'key': API_KEY,
        'part': 'snippet',
        'videoId': _videoId,
        'order': 'relevance',
        'textFormat': 'plaintext',
        'maxResults': 100,
    }

    response = requests.get(URL + 'commentThreads', params=params)
    resource = response.json()

    for item in resource['items']:
        text = item['snippet']['topLevelComment']['snippet']['textDisplay']
        comment_list.append([item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                             item['snippet']['topLevelComment']['snippet']['likeCount'],
                             item['snippet']['topLevelComment']['snippet']['textDisplay']])
    return comment_list

def dataList(_comment_list):
    if(_comment_list != []):
        param=['User name', 'Like count', 'text']
        df = pd.DataFrame(data = _comment_list,columns=param)
        df.to_csv("comments.csv")
        print('Output csv')
    else:
        print('None comment')

#実行
run()
