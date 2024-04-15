import requests
import re
from bs4 import BeautifulSoup
import json
import os
import time

WEBSITE_NAME        = "ifeng"
VIDEO_URL_PREFIX    = "https://v.ifeng.com/c/"
SEARCH_URL_PREFIX   = "https://so.ifeng.com/?q="

# 获取视频标题
def get_video_title(id):
    # 输入：视频 ID string
    # 输出：视频标题 string
    pass

# 获取视频简介
def get_video_intro(id):
    # 输入：视频 ID string
    # 输出：视频简介 string
    pass

# 获取视频播放量
def get_video_play(id):
    # 输入：视频 ID string
    # 输出：视频播放量和点赞量 string list
    pass

# 获取视频频道
def get_video_channel(id):
    # 输入：视频 ID string
    # 输出：视频频道 string
    pass

# 获取视频文件
def download_video_by_url(url):
    # 输入：视频 URL string
    # 输出：视频文件文件存储路径 string

    # 如果WEBSITE_NAME目录不存在那么创建WEBSITE_NAME目录
    if not os.path.exists("data/" + WEBSITE_NAME):
        os.makedirs("data/" + WEBSITE_NAME)
    file_path = "data/" + WEBSITE_NAME + "/" + url.split('/')[-1]
    return file_path

# 分段下载视频
def download_video(url):
    # 输入：视频 URL string
    # 输出：视频文件文件存储路径 string
    pass

# 搜索视频
def search_video(keyword):
    # 输入：搜索词 string
    # 输出：视频URL列表 list
    pass