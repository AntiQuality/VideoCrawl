import requests
import re
from bs4 import BeautifulSoup
import json
import os
import time

WEBSITE_NAME        = "ifeng"
VIDEO_URL_PREFIX    = "https://v.ifeng.com/c/{}"
VIDEO_LIKE_URL      = "https://survey.news.ifeng.com/api/getaccumulatorweight?key={}ding&format=js&serviceid=1"
SEARCH_URL_PREFIX   = "https://so.ifeng.com/?q={}"
SEARCH_API_URL      = "https://shankapi.ifeng.com/api/getSoFengData/video/{}/1/getSoFengDataCallback?callback=getSoFengDataCallback"
SEARCH_NUM          = 3

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
    title_div = soup.find('div', class_='index_titleInner_zF-mW')
    if title_div:
        title = title_div.h1.text
        return title
    else:
        return "未找到标题"

# 获取视频简介
def get_video_intro(id):
    # 输入：视频 ID string
    # 输出：视频简介 string
    return f"{WEBSITE_NAME} 没有简介"

# 将requests返回对象格式化为json数据
def format_response(response):
    data_str = response.content.decode('utf-8')
    json_str = data_str[data_str.find('{'):data_str.rfind('}')+1]
    parsed_data = json.loads(json_str)
    return parsed_data

# 获取视频播放量
def get_video_play(id):
    # 输入：视频 ID string
    # 输出：视频播放量和点赞量 string
    url = get_url(id)
    response = requests.get(url)
    guid = re.search(r'"docData":\s*\{[^}]*"vid":\s*"([^"]+)"', response.text).group(1)
    url = VIDEO_LIKE_URL.format(guid)
    response = requests.get(url)
    data = format_response(response)
    new_guid = f"{guid}ding"
    return f"{data['data']['browse'][new_guid]} 点赞"

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
    video_urls = re.search(r"img_video\" content=\"([^\"]*).mp4\"", response.text)
    video_url = video_urls.group(1)+".mp4"
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
    file_path = "logs/" + WEBSITE_NAME + "/" + WEBSITE_NAME + ".txt"
    with open(file_path, mode='a') as f:
        f.write(f"{id},{video_title},{video_intro},{video_play},{video_chan}\n")

# 搜索视频
def search_video(keyword):
    # 输入：搜索词 string
    # 输出：视频URL列表 list
    url = SEARCH_API_URL.format(keyword)
    video_list = []
    response = requests.get(url)
    # print(response.content)
    data = format_response(response)
    # print(json.dumps(data, indent=4, ensure_ascii=False))
    for num, item in enumerate(data['data']['items']):
    #    video_list.append(re.search(r"//ishare.ifeng.com/c/s/([^\"]*)", item['url']).group(1))
       video_list.append(item['id'])
       if num==SEARCH_NUM-1:
           break
    for id in video_list:
        get_video_info(id, '关键词')
    return video_list

if __name__ == '__main__':
    id = '7rl3FjbqxFY'
    id = '8YplFg0vM9f'
    keyword = '中东'
    get_video_info(id, 'ID')
    print(f"关键词 {keyword} 的搜索结果为：{search_video(keyword)}")
