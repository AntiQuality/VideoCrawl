if __name__ == '__main__':
    print('==========欢迎来到聚合视频下载系统！==========')
    website = input("请输入视频网站：")
    if website == 'haokan':
        import haokan as website
    elif website == 'thepaper':
        import thepaper as website
    elif website == 'ifeng':
        import ifeng as website
    elif website == 'xiaodutv':
        import xiaodutv as website
    elif website == 'ku6':
        import ku6 as website
    elif website == 'cntv':
        import cntv as website
    elif website == 'bilibili':
        import bilibili as website
    id = input("请输入视频ID：")
    keyword = input("请输入搜索词：")
    if id:
        website.get_video_info(id)
    elif keyword:
        website.search_video(keyword)
    else:
        print("请输入视频ID或搜索词...")