import haokan   as website_1
import thepaper as website_2
import ifeng    as website_3
import xiaodutv as website_4
import ku6      as website_5
import cntv     as website_6
import bilibili as website_7

keyword = "中东"
ids = ['12044787900912179135', '8474975156306847177', '8124860329860649270', '13970017207721920642', '10181684851484278141',
       '6881499675299249366', '5546765767744370513', '10181684851484278141', '16013430805600405183', '10151743800822807172']
for id in ids:
    website_1.get_video_info(id, 'ID')
website_1.search_video(keyword)

ids = ['27088645', '27088597', '27061593', '27061444', '27049839', '27061230', '27089461', '27089433', ]
for id in ids:
    website_2.get_video_info(id, 'ID')
website_2.search_video(keyword)

ids = []
for id in ids:
    website_3.get_video_info(id, 'ID')
website_3.search_video(keyword)

ids = []
for id in ids:
    website_4.get_video_info(id, 'ID')
website_4.search_video(keyword)

ids = []
for id in ids:
    website_5.get_video_info(id, 'ID')
website_5.search_video(keyword)

ids = []
for id in ids:
    website_1.get_video_info(id, 'ID')
website_1.search_video(keyword)

ids = []
for id in ids:
    website_6.get_video_info(id, 'ID')
website_6.search_video(keyword)

ids = []
for id in ids:
    website_7.get_video_info(id, 'ID')
website_7.search_video(keyword)