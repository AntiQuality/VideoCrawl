import requests
import re
from bs4 import BeautifulSoup
import json
import os
import time

WEBSITE_NAME        = "bilibili"
VIDEO_URL_PREFIX    = "https://www.bilibili.com/video/{}"
VIDEO_RES_URL       = "https://api.bilibili.com/x/player/playurl?fnval=80&avid={}&cid={}"
SEARCH_URL_PREFIX   = "https://search.bilibili.com/video?keyword={}"
SEARCH_API_URL      = "https://api.bilibili.com/x/web-interface/wbi/search/type?search_type=video&page=1&page_size=10&keyword={}"
SEARCH_NUM          = 1

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
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'referer': 'https://search.bilibili.com',
            'cookie': "buvid3=B12CDDF8-61AF-CD33-AFA9-C8C87FFCDC6519552infoc; LIVE_BUVID=AUTO7416572088582154; b_nut=100; CURRENT_FNVAL=4048; _uuid=846B1010DA-2C7A-4B810-10E7C-2FA6428CB81644606infoc; buvid4=33053282-471D-C646-6601-4FBC2CA69DD344997-024041510-Bi6Bn36okmRAw1fyEWgr%2BQ%3D%3D; PVID=2; b_lsid=51AB7810F_18EF0478AF4; enable_web_push=DISABLE; FEED_LIVE_VERSION=V_DYN_LIVING_UP; header_theme_version=CLOSE; home_feed_column=5; browser_resolution=1440-754; fingerprint=12c3f0b2883d5a0264ce2fba0ec48c40; buvid_fp_plain=undefined; rpdid=|(u)~lJJ|)k|0J'u~uJRk)kJl; buvid_fp=12c3f0b2883d5a0264ce2fba0ec48c40; SESSDATA=d67ee9a1%2C1728980519%2Cdd3bf%2A42CjAlrHUY4Ev6f3ksbdy92P0J47hiS584FLusYYIDEJ3caCVtmILYaqWTtoxFMqBbVmYSVlVSVlg1WmhNVHR6S1dnT3diLTMtQTVwdjEyWXRWM1FFMjFsRHQ0MVZNMW90YWNySkExc3NPdTloSFJrcFF4MmZDR2EyNGhwQ3lqTHVwUFhjWlRMZXlnIIEC; bili_jct=60c950400ebcdbd0f0b324ae4cb938eb; DedeUserID=524357591; DedeUserID__ckMd5=8981afce12622feb; sid=6rtpy9er; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTM2ODgyMjAsImlhdCI6MTcxMzQyODk2MCwicGx0IjotMX0.7CkVk8SSUXADoxHMkGnvbxLYDr0kg-Koz5w1pYb7nZ8; bili_ticket_expires=1713688160"
        }
        video_content = requests.get(url=url, headers=headers).content
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
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}
    url = get_url(id)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    value_div = soup.find('div', class_='video-info-title-inner')
    if value_div:
        value = value_div.h1.text               # 也可能没有h1
        return value
    else:
        return "未找到标题"

# 获取视频简介
def get_video_intro(id):
    # 输入：视频 ID string
    # 输出：视频简介 string
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}
    url = get_url(id)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    value_div = soup.find('span', class_='desc-info-text')
    if value_div:
        value = value_div.text               # 也可能没有h1
        return value
    else:
        return "未找到简介"

# 获取视频播放量
def get_video_play(id):
    # 输入：视频 ID string
    # 输出：视频播放量和点赞量 string
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}
    url = get_url(id)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    value_div = soup.find('div', class_='view-text')
    if value_div:
        value = value_div.text               # 也可能没有h1
        return f"{value} 播放"
    else:
        return "未找到播放量"

# 获取视频频道
def get_video_channel(id):
    # 输入：视频 ID string
    # 输出：视频频道 string
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}
    url = get_url(id)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    value_div = soup.find('div', class_='firstchannel-tag')
    if value_div:
        value = value_div.text               # 也可能没有h1
        return value
    else:
        return "未找到播放量"

# 根据当前视频网站决定下载方式
def download_video(id):
    # 输入：视频 URL string
    # 输出：视频文件文件存储路径 string
    filename = get_video_title(id) + ".mp4"
    url = get_url(id)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'referer': 'https://search.bilibili.com',
        'cookie': "buvid3=B12CDDF8-61AF-CD33-AFA9-C8C87FFCDC6519552infoc; LIVE_BUVID=AUTO7416572088582154; b_nut=100; CURRENT_FNVAL=4048; _uuid=846B1010DA-2C7A-4B810-10E7C-2FA6428CB81644606infoc; buvid4=33053282-471D-C646-6601-4FBC2CA69DD344997-024041510-Bi6Bn36okmRAw1fyEWgr%2BQ%3D%3D; PVID=2; b_lsid=51AB7810F_18EF0478AF4; enable_web_push=DISABLE; FEED_LIVE_VERSION=V_DYN_LIVING_UP; header_theme_version=CLOSE; home_feed_column=5; browser_resolution=1440-754; fingerprint=12c3f0b2883d5a0264ce2fba0ec48c40; buvid_fp_plain=undefined; rpdid=|(u)~lJJ|)k|0J'u~uJRk)kJl; buvid_fp=12c3f0b2883d5a0264ce2fba0ec48c40; SESSDATA=d67ee9a1%2C1728980519%2Cdd3bf%2A42CjAlrHUY4Ev6f3ksbdy92P0J47hiS584FLusYYIDEJ3caCVtmILYaqWTtoxFMqBbVmYSVlVSVlg1WmhNVHR6S1dnT3diLTMtQTVwdjEyWXRWM1FFMjFsRHQ0MVZNMW90YWNySkExc3NPdTloSFJrcFF4MmZDR2EyNGhwQ3lqTHVwUFhjWlRMZXlnIIEC; bili_jct=60c950400ebcdbd0f0b324ae4cb938eb; DedeUserID=524357591; DedeUserID__ckMd5=8981afce12622feb; sid=6rtpy9er; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTM2ODgyMjAsImlhdCI6MTcxMzQyODk2MCwicGx0IjotMX0.7CkVk8SSUXADoxHMkGnvbxLYDr0kg-Koz5w1pYb7nZ8; bili_ticket_expires=1713688160"
    }

    response = requests.get(url, headers=headers)
    data = re.search(r"__INITIAL_STATE__=({.*});\(function", response.text)
    json_data = json.loads(data.group(1))
    cid = json_data['videoData']['pages'][0]['cid']
    aid = json_data['videoData']['aid']

    url = VIDEO_RES_URL.format(aid, cid)

    response = requests.get(url, headers=headers)
    data = json.loads(response.content.decode('utf-8'))
    video_url = data['data']['dash']['video'][0]['baseUrl']
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
    print(f"视频所属频道是：{video_chan}")
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
    url = SEARCH_API_URL.format(keyword)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'referer': 'https://search.bilibili.com/video?keyword=%E4%B8%AD%E4%B8%9C',
        'cookie': "buvid3=B12CDDF8-61AF-CD33-AFA9-C8C87FFCDC6519552infoc; LIVE_BUVID=AUTO7416572088582154; b_nut=100; CURRENT_FNVAL=4048; _uuid=846B1010DA-2C7A-4B810-10E7C-2FA6428CB81644606infoc; buvid4=33053282-471D-C646-6601-4FBC2CA69DD344997-024041510-Bi6Bn36okmRAw1fyEWgr%2BQ%3D%3D; PVID=2; b_lsid=51AB7810F_18EF0478AF4; enable_web_push=DISABLE; FEED_LIVE_VERSION=V_DYN_LIVING_UP; header_theme_version=CLOSE; home_feed_column=5; browser_resolution=1440-754; fingerprint=12c3f0b2883d5a0264ce2fba0ec48c40; buvid_fp_plain=undefined; rpdid=|(u)~lJJ|)k|0J'u~uJRk)kJl; buvid_fp=12c3f0b2883d5a0264ce2fba0ec48c40; SESSDATA=d67ee9a1%2C1728980519%2Cdd3bf%2A42CjAlrHUY4Ev6f3ksbdy92P0J47hiS584FLusYYIDEJ3caCVtmILYaqWTtoxFMqBbVmYSVlVSVlg1WmhNVHR6S1dnT3diLTMtQTVwdjEyWXRWM1FFMjFsRHQ0MVZNMW90YWNySkExc3NPdTloSFJrcFF4MmZDR2EyNGhwQ3lqTHVwUFhjWlRMZXlnIIEC; bili_jct=60c950400ebcdbd0f0b324ae4cb938eb; DedeUserID=524357591; DedeUserID__ckMd5=8981afce12622feb; sid=6rtpy9er; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTM2ODgyMjAsImlhdCI6MTcxMzQyODk2MCwicGx0IjotMX0.7CkVk8SSUXADoxHMkGnvbxLYDr0kg-Koz5w1pYb7nZ8; bili_ticket_expires=1713688160"
    }

    response = requests.get(url, headers=headers)
    data = json.loads(response.content.decode('utf-8'))
    for num, id in enumerate(data['data']['result']):
        video_list.append(id['bvid'])
        if num==SEARCH_NUM-1:
            break

    for id in video_list:
        get_video_info(id, '关键词')
    return video_list

if __name__ == '__main__':
    id = 'BV1sJ4m1j7SP'
    keyword = '中东'
    get_video_info(id, 'ID')
    print(f"关键词 {keyword} 的搜索结果为：{search_video(keyword)}")