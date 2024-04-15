# 开发一个或多个爬虫脚本，可以根据输入的视频节目的 ID 和搜索词，自动爬取对应视频网站中的该视频节目 ID\该搜索词搜索下视频的标题、简介、播放量、频道和视频文件等。
# 为实现上述目标，请分析目标网站的结构，针对下述网站自动获取不同视频节目信息。
# 注意：本任务目的是使大家熟悉主动获取技术，不得将爬取结果公开或商用。

# 目标网站
# v.ifeng.com 凤凰网
# v.xiaodutv.com 百搜视频
# www.thepaper.cn 澎湃网，视频在https://www.thepaper.cn/channel_26916
# haokan.baidu.com 好看视频
# www.ku6.com 酷6网
# tv.cntv.cn 央视网
# www.bilibili.com 哔哩哔哩

# 分数评价标准
# 序号 完成内容 得分
# 1 获取节目标题 2
# 2 获取节目简介 2
# 3 获取节目播放量\点赞数 5
# 4 获取节目所属频道 1
# 5 固定 URL 视频文件获取 2
# 6 分段传输视频节目获取 3
# 7 按搜索词批量获取上述内容 5
# 8 任务报告 5
# 9 PPT 汇报 5


# 不同网站所用到的共性函数

import requests
import re
from bs4 import BeautifulSoup
import json
import os
import time

WEBSITE_NAME        = ""
VIDEO_URL_PREFIX    = ""
SEARCH_URL_PREFIX   = ""

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
    pass

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

# Python代码

# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup
import json
import os
import time

class Crawler:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        self.video_list = []

    def get_video_info(self, url):
        response = requests.get(url, headers=self.headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('title').get_text()
        description = soup.find('meta', {'name': 'description'})['content']
        play_count = soup.find('span', {'class': 'play-count'}).get_text()
        channel = soup.find('a', {'class': 'channel'}).get_text()
        video_url = re.search(r'videoUrl: "(.*?)"', response.text).group(1)
        video_info = {
            'title': title,
            'description': description,
            'play_count': play_count,
            'channel': channel,
            'video_url': video_url
        }
        self.video_list.append(video_info)

    def get_video_list(self, keyword):
        url = 'https://v.ifeng.com/search/?q=' + keyword
        response = requests.get(url, headers=self.headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        video_list = soup.find_all('div', {'class': 'search-list'})
        for video in video_list:
            video_url = video.find('a')['href']
            self.get_video_info(video_url)

    def save_video_info(self):
        with open('video_info.json', 'w', encoding='utf-8') as f:
            json.dump(self.video_list, f, ensure_ascii=False)

    def download_video(self):
        for video in self.video_list:
            video_url = video['video_url']
            video_name = video['title']
            response = requests.get(video_url, headers=self.headers)
            with open(video_name + '.mp4', 'wb') as f:
                f.write(response.content)
            time.sleep(1)

if __name__ == '__main__':
    crawler = Crawler()
    crawler.get_video_list('python')
    crawler.save_video_info()
    crawler.download_video()