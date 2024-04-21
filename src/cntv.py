import requests
import re
from bs4 import BeautifulSoup
import json
import os
import time

WEBSITE_NAME        = "cntv"
VIDEO_URL_PREFIX    = "https://tv.cctv.com/{}.shtml"
VIDEO_LIKE_URL      = "https://api.itv.cntv.cn/praise/add?type=other&id={}&num=1&jsonp_callback=cb&jsonp_callback=dianzan"
MAIN_m3u8_URL       = "https://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?pid={}"
VIDEO_TS_URL        = "https://hls.cntv.kcdnvip.com{}"
SEARCH_URL_PREFIX   = "https://search.cctv.com/search.php?qtext={}&type=video"
SEARCH_API_URL      = "https://search.cctv.com/ifsearch.php?page=1&qtext={}&sort=relevance"
SEARCH_NUM          = 10

# 根据视频id得到视频url
def get_url(id):
    return VIDEO_URL_PREFIX.format(id)

# 初始化视频文件存储路径
def initial_video_by_url(filename):
    # 输入：视频文件名 string
    # 输出：无
    if not os.path.exists("data/" + WEBSITE_NAME):
        os.makedirs("data/" + WEBSITE_NAME)
    file_path = "data/" + WEBSITE_NAME + "/" + filename
    with open(file_path, mode='w') as f:
        print("初始化视频文件路径：", file_path)

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
    # 注意cntv的多段ts视频合并下载是append
    with open(file_path, mode='ab') as f:
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
    print('\t',id)
    response = requests.get(url)
    soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')
    value_div = soup.find('div', class_='tit')        # 取决于网站结构
    if value_div:
        value = value_div.text               # 也可能没有h1
        return value
    else:
        return "未找到标题"

# 获取视频简介
def get_video_intro(id):
    # 输入：视频 ID string
    # 输出：视频简介 string
    url = VIDEO_URL_PREFIX.format(id)

    # # v.cctv.com
    # print(url)
    # response = requests.get(url)
    # intro_tag = re.search(r"var videobrief=\"([^\"]*)\"", response.content.decode('utf-8'))
    # return intro_tag.group(1)

    # tv.cctv.com
    response = requests.get(url)
    soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')
    value_div = soup.find('div', class_='video_brief')        # 取决于网站结构
    if value_div:
        value = value_div.text               # 也可能没有h1
        return value
    else:
        return "未找到简介"

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
    id = id.split('/')[-1]
    url = VIDEO_LIKE_URL.format(id)
    response = requests.get(url)
    data = format_response(response)
    return f"{data['data']['num']} 点赞"

# 获取视频频道
def get_video_channel(id):
    # 输入：视频 ID string
    # 输出：视频频道 string
    return f"{WEBSITE_NAME} 没有频道"

# 得到cntv当前视频的guid
def get_guid(id):
    # 输入：视频 ID string
    # 输出：视频 guid string
    url = get_url(id)
    response = requests.get(url)
    data = response.content.decode('utf-8')
    value = re.search(r"var guid = \"([^\"]*)\"", data)
    return value.group(1)

# 通过guid获取当前视频的主m3u8，并得到真实的次级m3u8文件URL片段
def get_actual_m3u8(guid):
    # 输入：当前视频的guid string
    # 输出：可用的次级m3u8文件URL片段 string
    url = MAIN_m3u8_URL.format(guid)

    response = requests.get(url)
    data = json.loads(response.content.decode('utf-8'))

    url = data["hls_url"]

    response = requests.get(url)
    data = response.content.decode('utf-8')
    value = "/asp"+re.search(r"/asp([^.]*).m3u8", data).group(1)+".m3u8"
    return value

# 通过可用的次级m3u8片段，拼接后读取ts文件列表
def get_ts_list(url_chip):
    # 输入：可用的次级m3u8文件URL片段 string
    # 输出：该视频的ts文件列表 list
    url = VIDEO_TS_URL.format(url_chip)
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Cookie": "brstaut=undefined; HMF_CI=7bedd0cf4f4f96fdb4b4683ed6878f6e531e69bc86e5d6cea423e3a9dd36d533617e481459c26a1aec611d2efb63cec8bd9af332a0db7691483a1709482e0f2fd7; HMY_JC=5d1a89cb578bcdb4b45c7eba82df3161339218b09ff548c2ea8c6e2798ed3a5c85,; HBB_HC=01c7c9c4bdcd2277d98e1b814b5a91d42eaf5f5c19c03e65fc917ede072f1b48fa46c0fb3e7b199a46e725b16c85e527c7",
        "referrer": "https://tv.cctv.com/"
    }
    response = requests.get(url, headers=headers)
    data = response.content.decode('utf-8')
    return re.findall(r"\d+\.ts", data)

# 根据当前视频网站决定下载方式
def download_video(id):
    # 输入：视频 URL string
    # 输出：视频文件文件存储路径 string
    guid = get_guid(id)
    m3u8_url = get_actual_m3u8(guid)
    ts_list = get_ts_list(m3u8_url)

    filename = get_video_title(id) + ".mp4"
    m3u8_url_without = VIDEO_TS_URL.format(m3u8_url)
    m3u8_url_without = m3u8_url_without[:m3u8_url_without.rfind('/')]+'/'
    res = []
    initial_video_by_url(filename)
    for ts in ts_list:
        ts_url = m3u8_url_without+ts
        print(f"视频URL：{ts_url}")
        res.append(download_video_by_url(ts_url, filename))
    return res[0]
    # url = get_url(id)
    # response = requests.get(url)
    # video_urls = re.search(r"img_video\" content=\"([^\"]*).mp4\"", response.text)
    # video_url = video_urls.group(1)+".mp4"
    # print(f"视频URL：{video_url}")
    # return download_video_by_url(video_url, filename)

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
    title_set = set()
    video_list = []
    num = 0

    response = requests.get(url)
    str = response.content.decode('utf-8')
    data = json.loads(str)
    for item in data['list']:
        if item['all_title'] in title_set:
            continue
        title_set.add(item['all_title'])
        value = re.search(r".com/([^\"]*).shtml", item['urllink'])
        video_list.append(value.group(1))
        num += 1
        if num==SEARCH_NUM:
            break

    for id in video_list:
        get_video_info(id, '关键词')
    return video_list

if __name__ == '__main__':
    # id = '2024/04/17/VIDEvHc3qIZvsOiCk7qtxpAl240417'
    id = '2024/04/18/VIDE5n5Lbl1QoCD2K922xnS8240418'
    keyword = '中东'
    get_video_info(id, 'ID')
    print(f"关键词 {keyword} 的搜索结果为：{search_video(keyword)}")