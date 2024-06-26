import requests
import re
from bs4 import BeautifulSoup
import json
import os
import time
from urllib.parse import unquote

WEBSITE_NAME        = "xiaodutv"
VIDEO_URL_PREFIX    = "https://v.xiaodutv.com/watch/{}.html"
SEARCH_URL_PREFIX   = ""
SEARCH_API_URL      = "https://haokan.baidu.com/haokan/ui-search/pc/search/video?pn=2&rn=10&type=video&query={}"
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
    title_div = soup.find('div', class_='title-cont')        # 取决于网站结构
    if title_div:
        title = title_div.h2.text               # 也可能没有h1
        return title
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
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    value_div = soup.find('span', class_='num play')        # 取决于网站结构
    if value_div:
        value = value_div.text               # 也可能没有h1
        value = value.replace('\n','').replace('\r','').replace('\t','')
        return value
    else:
        return "未找到播放量"

# 获取视频频道
def get_video_channel(id):
    # 输入：视频 ID string
    # 输出：视频频道 string
    return f"{WEBSITE_NAME} 没有频道"

# 根据当前视频网站决定下载方式
def download_video(id):
    # 输入：视频 URL string
    # 输出：视频文件文件存储路径 string
    filename = get_video_title(id) + ".mp4"
    url = get_url(id)
    response = requests.get(url)
    video_urls = re.search(r"fullscreen&video=([^\"]*)\';", response.text)
    video_url = unquote(video_urls.group(1))
    print(f"视频URL：{video_url}")
    return download_video_by_url(video_url, filename)

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
    }
    param = {
        'sign' : 'bb78c93f7ed6d9e54138326682823eac',
        'timestamp' : '1713355699714',
        'version' : '1'
    }
    response = requests.get(url, headers=headers, params=param)
    data = json.loads(response.content.decode('utf-8'))
    for num, item in enumerate(data['data']['list']):
        # print(f"{num+1}. {item['vid']}")
        video_list.append(item['vid'])
        if num==SEARCH_NUM-1:
           break
    
    print(video_list)
    from haokan import get_video_info as get_video_info_haokan
    
    for id in video_list:
        get_video_info_haokan(id, '关键词', WEBSITE_NAME='xiaodutv')
    return video_list

if __name__ == '__main__':
    id = '05346747067631501098'
    keyword = '中东'
    # get_video_info(id)
    print(f"关键词 {keyword} 的搜索结果为：{search_video(keyword)}")