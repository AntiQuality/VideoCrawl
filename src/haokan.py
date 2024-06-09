import requests
import re
from bs4 import BeautifulSoup
import json
import os
import time

WEBSITE_NAME        = "haokan"
VIDEO_URL_PREFIX    = "https://haokan.baidu.com/v?vid={}"
SEARCH_URL_PREFIX   = "https://haokan.baidu.com/web/search/page?query={}"
# SEARCH_API_URL      = "https://haokan.baidu.com/haokan/ui-search/pc/search/video?pn=1&rn=10&type=video&query={}"
SEARCH_API_URL      = "https://haokan.baidu.com/haokan/ui-search/pc/search/video?pn=1&rn=10&type=video&query={}&sign=f8b6a52bb5f38c55b86856852689dfc2&version=1&timestamp=1713714943502"
SEARCH_NUM          = 10

# 根据视频id得到视频url
def get_url(id):
    return VIDEO_URL_PREFIX.format(id)

# 获取视频文件
def download_video_by_url(url, filename=None, WEBSITE_NAME=WEBSITE_NAME):
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
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    value_div = soup.find('div', class_='ssr-video-title')
    if value_div:
        value = value_div.text               # 也可能没有h1
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
    url = get_url(id)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    value_div = soup.find('div', class_='ssr-extrainfo')
    if value_div:
        value = value_div.text               # 也可能没有h1
        value = value.split(' ')[0]
        return value
    else:
        return "未找到播放量"

# 获取视频频道
def get_video_channel(id):
    # 输入：视频 ID string
    # 输出：视频频道 string
    return f"{WEBSITE_NAME} 没有频道"

# 根据当前视频网站决定下载方式
def download_video(id, WEBSITE_NAME=WEBSITE_NAME):
    # 输入：视频 URL string
    # 输出：视频文件文件存储路径 string
    filename = get_video_title(id) + ".mp4"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    }
    suffix = '&_format=json&hk_nonce=f39f03e3edd2e4b3f7670c131c23eb93&hk_timestamp=1713364549&hk_sign=b706bd67b0962a06edf626d6b2b2075f&hk_token=f297dAVwdwNzCnYBcHdyABAHDQA'
    url = get_url(id)+suffix
    response = requests.get(url, headers=headers)
    data = json.loads(response.content.decode('utf-8'))
    # print(data['data']['apiData']['curVideoMeta']['playurl'])
    video_url = data['data']['apiData']['curVideoMeta']['playurl']
    print(f"视频URL：{video_url}")
    return download_video_by_url(video_url, filename, WEBSITE_NAME=WEBSITE_NAME)

# 收集视频基本信息
def get_video_info(id, title='ID', WEBSITE_NAME=WEBSITE_NAME):
    title = f'-----根据 {title} 获取视频信息-----'
    video_title = get_video_title(id)
    video_intro = get_video_intro(id)
    video_play  = get_video_play(id)
    video_chan  = get_video_channel(id)
    video_path  = download_video(id, WEBSITE_NAME=WEBSITE_NAME)
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
    file_path = "logs/" + WEBSITE_NAME + "/" + WEBSITE_NAME + ".csv"
    with open(file_path, mode='a') as f:
        f.write(f"{id},{video_title},{video_intro},{video_play},{video_chan}\n")

# 搜索视频
def search_video(keyword):
    # 输入：搜索词 string
    # 输出：视频URL列表 list
    video_list = []
    num = 0

    url = SEARCH_API_URL.format(keyword)
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    }
    param = {
        'sign' : 'f8b6a52bb5f38c55b86856852689dfc2',
        'version' : '1',
        'timestamp' : '1713714943502'
    }

    # response = requests.get(url, headers=headers, params=param)
    # print(url)
    response = requests.get(url, headers=headers)
    data = json.loads(response.content.decode('utf-8'))
    print(data)
    for num, item in enumerate(data['data']['list']):
        # print(f"{num+1}. {item['vid']}")
        video_list.append(item['vid'])
        if num==SEARCH_NUM-1:
           break
    for id in video_list:
        get_video_info(id, '关键词')
    return video_list

if __name__ == '__main__':
    id = '14132403750757824877'
    keyword = '中东'
    get_video_info(id, 'ID')
    print(f"关键词 {keyword} 的搜索结果为：{search_video(keyword)}")