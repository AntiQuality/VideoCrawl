# 开发一个或多个爬虫脚本，可以根据输入的视频节目的 ID 和搜索词，自动爬取对应视频网站中的该视频节目 ID\该搜索词搜索下视频的标题、简介、播放量、频道和视频文件等。
# 为实现上述目标，请分析目标网站的结构，针对下述网站自动获取不同视频节目信息。
# 注意：本任务目的是使大家熟悉主动获取技术，不得将爬取结果公开或商用。

# 目标网站
# v.ifeng.com 凤凰网
# v.xiaodutv.com 百搜视频
# www.thepaper.cn 澎湃网，视频在https://www.thepaper.cn/channel_26916
# haokan.baidu.com 好看视频
# www.ku6.com 酷6网
# tv.cntv.cn 央视网，视频在https://v.cctv.com
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
SEARCH_API_URL      = ""
SEARCH_NUM          = 10

# 根据视频id得到视频url
def get_url(id):
    return VIDEO_URL_PREFIX.format(id)

# 获取视频文件
def download_video_by_url(url, filename=None):
    # 输入：视频 URL string；视频文件名 string（可选）
    # 输出：视频文件存储路径 string

    if filename is None:
        filename = url.split('/')[-1]

    # 如果WEBSITE_NAME目录不存在那么创建WEBSITE_NAME目录
    if not os.path.exists("data/" + WEBSITE_NAME):
        os.makedirs("data/" + WEBSITE_NAME)
    file_path = "data/" + WEBSITE_NAME + "/" + filename
    with open(file_path, mode='wb') as f:
        print(f'\t正在保存{WEBSITE_NAME}视频：{filename}')
        video_content = requests.get(url=url).content
        f.write(video_content)
        print(f'\t成功保存{WEBSITE_NAME}视频：{filename}')

    return file_path

# 分段下载视频
def download_video_by_segment(url, filename=None):
    # 输入：视频 URL string；视频文件名 string（可选）
    # 输出：视频文件存储路径 string
    
    if filename is None:
        filename = url.split('/')[-1]

    # 如果WEBSITE_NAME目录不存在那么创建WEBSITE_NAME目录
    if not os.path.exists("data/" + WEBSITE_NAME):
        os.makedirs("data/" + WEBSITE_NAME)
    file_path = "data/" + WEBSITE_NAME + "/" + filename
    return file_path

# 获取视频标题
def get_video_title(id):
    # 输入：视频 ID string
    # 输出：视频标题 string
    url = get_url(id)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    value_div = soup.find('', class_='')        # 取决于网站结构
    if value_div:
        value = value_div.h1.text               # 也可能没有h1
        return value
    else:
        return "未找到标题"

# 获取视频简介
def get_video_intro(id):
    # 输入：视频 ID string
    # 输出：视频简介 string
    return f"{WEBSITE_NAME} 没有简介"

# 获取视频播放量
def get_video_play(id):
    # 输入：视频 ID string
    # 输出：视频播放量和点赞量 string
    pass

# 获取视频频道
def get_video_channel(id):
    # 输入：视频 ID string
    # 输出：视频频道 string
    return f"{WEBSITE_NAME} 没有频道"

# 根据当前视频网站决定下载方式
def download_video(id):
    # 输入：视频 URL string
    # 输出：视频文件文件存储路径 string
    pass

# 收集视频基本信息
def get_video_info(id, title='ID'):
    title = f'-----根据 {title} 获取视频信息-----'
    video_title = get_video_title(id)
    video_intro = get_video_intro(id)
    video_play  = get_video_play(id)
    video_chan  = get_video_channel(id)
    video_path  = download_video(id)
    print(title)
    print(f"视频标题是：{video_title}")
    print(video_intro)
    print(video_play)
    print(video_chan)
    print(f"视频存储路径：{video_path}")
    if not os.path.exists("logs/" + WEBSITE_NAME):
        os.makedirs("logs/" + WEBSITE_NAME)
    file_path = "logs/" + WEBSITE_NAME + "/" + video_title + '.txt'
    with open(file_path, mode='w') as f:
        f.write(title+'\n')
        f.write(f"ID：{id}\n")
        f.write(f'标题：{video_title}\n')
        f.write(f'简介：{video_intro}\n')
        f.write(f'点赞/播放量：{video_play}\n')
        f.write(f'频道：{video_chan}\n')
        print(f'{WEBSITE_NAME}视频日志存储：{file_path}')

# 搜索视频
def search_video(keyword):
    # 输入：搜索词 string
    # 输出：视频URL列表 list
    video_list = []
    for id in video_list:
        get_video_info(id, '关键词')
    return video_list

if __name__ == '__main__':
    id = ''
    keyword = ''
    get_video_info(id, 'ID')
    print(f"关键词 {keyword} 的搜索结果为：{search_video(keyword)}")