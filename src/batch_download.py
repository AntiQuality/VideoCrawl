import haokan   as website_1
import thepaper as website_2
import ifeng    as website_3
import xiaodutv as website_4
import ku6      as website_5
import cntv     as website_6
import bilibili as website_7

keyword = "中东"

ids = ['12044787900912179135', '8474975156306847177', '8124860329860649270', '13970017207721920642', '10181684851484278141',
       '6881499675299249366', '5546765767744370513', '17544423368322312949', '16013430805600405183', '10151743800822807172']
for id in ids:
    website_1.get_video_info(id, 'ID')
website_1.search_video(keyword)

ids = ['27088645', '27088597', '27061593', '27061444', '27049839', '27061230', '27089461', '27089433', '27110780', '27112334']
for id in ids:
    website_2.get_video_info(id, 'ID')
website_2.search_video(keyword)

ids = ['8Yy8RpHWUZ9', '8YxEFr821sQ', '8Yy7iuTWveN', '8YxuUVwIzdX', '8YyHgR4KcXH', '8YyMdfR2q3I', '8YuGVGGfyyc', '8Xu1LFhVagH', '8YyKvgT3zlh', '8YyC3tBycJF']
for id in ids:
    website_3.get_video_info(id, 'ID')
website_3.search_video(keyword)

ids = ['01913472023966969006', '05647894352904460140', '4474262132727135423', '01788121390023820047', '06319272425809636111',
'485332083435397018', '0175533126662579170', '05742620249840630164', '8899328622737480156', '8343090255389640201']
for id in ids:
    website_4.get_video_info(id, 'ID')
website_4.search_video(keyword)

ids = ['J1Bpikg6SUYCoO1kHwnzStPBHtg', '0kBZ8kWbgmV-Fr24u9XUgzBPVHg', '44vYsM7UBVAEZ8ZbQ4r_k5-4nbw',
'37i59RdhW_xXuCzphK4bfnNnC3I', 'l-hm6HsK4uJZmI8bSlNr3k160-g', 'iLJrbxKr9rLXN1aX22frRMr7C6E',
'lqmYxHeTTC9x8PuII06TMgDBQhQ', 'zFWzGxx9iLBtNtJI08Rx82WiySo', '6kpMeoBNu8DC7Rp6Tw0B7XxVVuU',
'P67b-grgasqqc3YhVp8CEnR_FvI']
for id in ids:
    website_5.get_video_info(id, 'ID')
website_5.search_video(keyword)

ids = ['2024/04/21/VIDE7bV77HdP2kxxYB0C288I240421', '2024/04/20/VIDEeNKkWrgEjdvskHAcE88G240420', 
       '2024/04/20/VIDEfkhg66mUN1FBBaN1G1re240420', '2024/04/20/VIDEjyfIGV3TERytDe6b9sYH240420',
       '2024/04/20/VIDEo1rLAvT1zyCSglb489nl240420', '2024/04/21/VIDEf0RCHADGit1G01vofb0d240421',
       '2024/04/22/VIDE0oEa1Uwdvo1wMJEU8ivv240422', '2024/04/21/VIDEgW5dYNyXJio2mrGRApDx240421',
       '2024/04/21/VIDEYVVhjpxyCMmuc1gSXknZ240421', '2024/04/21/VIDEfF7FpuwqyyOzcUJSeNvJ240421']
for id in ids:
    website_6.get_video_info(id, 'ID')
website_6.search_video(keyword)

ids = ['BV1Vi421f7Go', 'BV1dS4y1P7h7', 'BV1c3411Q7XH', 'BV1VE411j7wk', 'BV1GC41137fv',
'BV1CP4y1W7WJ', 'BV16H4y1K7tJ', 'BV1f8411c7Bx', 'BV1LF411f7TW', 'BV1fK4y1c7xT']
for id in ids:
    website_7.get_video_info(id, 'ID')
website_7.search_video(keyword)