#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/13 10:15 下午
# @Author  : jianwei.lv

import requests
from datetime import datetime
import time
import os

# 关注的博主用户名列表 https://xueqiu.com/u/8940371568
# 博主名：id
bloggers = {
    # "投研家": "8940371568",
    # "万得调研": "4198802945",
    # "雪月霜": "1505944393",
    "投研与逻辑": "2852344450",
    "寒山invest": "5441610555",
    "雷雨季节": "1072107809",
    "花盆君": "5452093377",
    "合理出奇迹": "1708120238",
    # "十年七倍": "9821253825",
    "周期合伙人": "6347482150",
    # "UESTC独钓寒江雪": "2377563498",
    "密探一号": "9999782882",
    "三生万物时": "1695241710",
    "洒脱的古龙": "7977236763",
    "斯卡纳贝": "3352558222",
    "乘黄18": "3945042689",
    "银河投递员": "1718809686",
    "双子窥天新号": "3849856324",
    "鲨鱼哥的视频逻辑": "7447535920",
    "无心0000": "8069880019",
    "无鸣之辈-阿飞": "4253976756",
    "本股神": "1819336967",
    "轮回666": "8282709675",
    "疯狂梭哈哥": "8282709675",
    "rtu8": "2759777767",
    "慢而坚定-杯柄vcp": "9998407395",
    "zk0325": "2125333315",
    "小小草008": "4198283442",
    "冰冰小美": "7143769715",
    "游资呼家楼": "7734132744",
    "交易逻辑掌门": "2543519410",
    "准九": "4279190191",
    "TDK168": "3463940412",
    "好习惯受用终生": "4015596010",
    "行中衡": "271398626",
    "子渊如墨": "1905287979",
    "睿钞观察": "7556690213",
    "社会性动物": "6141010503",
    "永远的冠军": "3666837602",
    "金如意": "3658116657",
    "谭校长专注投资理财": "1734585936",
    "复利子": "6461763781",
    "方知方觉": "6327693894",
    "德玛小王": "4891560143",
    "皈依凡尘": "8560060423",
    "花花牛2016": "7824196356",
    "啊流浪猫": "278149183",
    "燕云2021": "1034624503",
    "抢财猫": "3270941735",
    "小盘教父": "8714944821",
    "黑猫投资": "9603434293",
    "神猫识顶底": "8350226665",
    "小股民c": "9465171998",
    "临渊巷13号": "9136627432",
    "交易鹿": "6089882321",
    "民侦探小吴": "7219493166",
    "王增森": "1465420860"
}

spBloggers = {
    "神猫识顶底": "8350226665",
    "TDK168": "3463940412",
    "子渊如墨": "1905287979",
    "慢而坚定-杯柄vcp": "9998407395",
    "小盘教父": "8714944821",
    "黑猫投资": "9603434293",
    "小股民c": "9465171998",
    "德玛小王": "4891560143",
}
# 发言提示URL
bloggers_url = "https://xueqiu.com/v4/statuses/user_timeline.json?user_id={0}&page={1}"

# 请求头信息

cookies = {
    '__utmz': '1.1679307632.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    'cookiesu': '251692352267798',
    'u': '3058190831',
    'xq_is_login': '1',
    '__utma': '1.1859006477.1679307632.1710225210.1710311362.125',
    'device_id': '2f7ac20a537c2ded20902d3cd5e51ff8',
    's': 'by12f7uto3',
    'bid': 'f2482796a6eda57a039c2760d1448818_lu2bqv1s',
    'xq_a_token': 'cf0b5e98aab56abff210e1457a5c1835a7f3bb63',
    'xqat': 'cf0b5e98aab56abff210e1457a5c1835a7f3bb63',
    'xq_id_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjMwNTgxOTA4MzEsImlzcyI6InVjIiwiZXhwIjoxNzEzNzg3Mjc2LCJjdG0iOjE3MTExOTUyNzY4MjgsImNpZCI6ImQ5ZDBuNEFadXAifQ.oUsyJzOIuyVfF0dXT7PZzgFxPoYoEGWX2Fyb_tbxuZd2YP_Xs07x1_6ysWZgD8OVS5hxpqU17-YABOtAqfsvho4JMXzmHpJh0u18IEAHYoy_dShhbOJCFXWsc567vryA7Z5NX6vKyYD32j7Xn4_W1WznLfDEJtxfZb0bPGr3bca0R3Rcak9wt8gCNJiEITQddZkEtQiePc4yO8YRo_7kV6BIVTaOf1_4LPSwbIPT2QJSgf4_nWyvonWFLy4nnF49yLgs9il0bKY8f-UOIlbHYIh0Kf5OQaxu1CzNVOm_fYjSLevQKF9zclyS0y1p2Prj7YpdejbOOuqi56uc8uxu3g',
    'xq_r_token': 'feb719475c7c17eb07bc590fa80baeac2c8c4c3b',
    'snbim_minify': 'true',
    'Hm_lvt_1db88642e346389874251b5a1eded6e3': '1711198388',
    'acw_tc': '2760827617115953495463796ec1911343194c791c33e3354aec56a78e4b6e',
    'smidV2': '20240328110910eed3e913fd3a3380b7a16717b8b63dab00e2473dc279c4290',
    'is_overseas': '0',
    'Hm_lpvt_1db88642e346389874251b5a1eded6e3': '1711595591',
    '.thumbcache_f24b8bbe5a5934237bbc0eda20c1b6e7': 'P58hf1nU48YYUuBQOslQk5Un87H+IcJlBuPN37pT9UmJxs5KNaApCjGE2RhTAnbPlu8CVhUKJjN8PnLRGPz5pw%3D%3D',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    # 'Cookie': '__utmz=1.1679307632.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); cookiesu=251692352267798; u=3058190831; xq_is_login=1; __utma=1.1859006477.1679307632.1710225210.1710311362.125; device_id=2f7ac20a537c2ded20902d3cd5e51ff8; s=by12f7uto3; bid=f2482796a6eda57a039c2760d1448818_lu2bqv1s; xq_a_token=cf0b5e98aab56abff210e1457a5c1835a7f3bb63; xqat=cf0b5e98aab56abff210e1457a5c1835a7f3bb63; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjMwNTgxOTA4MzEsImlzcyI6InVjIiwiZXhwIjoxNzEzNzg3Mjc2LCJjdG0iOjE3MTExOTUyNzY4MjgsImNpZCI6ImQ5ZDBuNEFadXAifQ.oUsyJzOIuyVfF0dXT7PZzgFxPoYoEGWX2Fyb_tbxuZd2YP_Xs07x1_6ysWZgD8OVS5hxpqU17-YABOtAqfsvho4JMXzmHpJh0u18IEAHYoy_dShhbOJCFXWsc567vryA7Z5NX6vKyYD32j7Xn4_W1WznLfDEJtxfZb0bPGr3bca0R3Rcak9wt8gCNJiEITQddZkEtQiePc4yO8YRo_7kV6BIVTaOf1_4LPSwbIPT2QJSgf4_nWyvonWFLy4nnF49yLgs9il0bKY8f-UOIlbHYIh0Kf5OQaxu1CzNVOm_fYjSLevQKF9zclyS0y1p2Prj7YpdejbOOuqi56uc8uxu3g; xq_r_token=feb719475c7c17eb07bc590fa80baeac2c8c4c3b; snbim_minify=true; Hm_lvt_1db88642e346389874251b5a1eded6e3=1711198388; acw_tc=2760827617115953495463796ec1911343194c791c33e3354aec56a78e4b6e; smidV2=20240328110910eed3e913fd3a3380b7a16717b8b63dab00e2473dc279c4290; is_overseas=0; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1711595591; .thumbcache_f24b8bbe5a5934237bbc0eda20c1b6e7=P58hf1nU48YYUuBQOslQk5Un87H+IcJlBuPN37pT9UmJxs5KNaApCjGE2RhTAnbPlu8CVhUKJjN8PnLRGPz5pw%3D%3D',
    'Referer': 'https://xueqiu.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'elastic-apm-traceparent': '00-3e86e4b15da390e89e40b556c42437e6-d1d6dfbba074e16e-00',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}



def get_bloggers_status(bloggers, commit_time, page=1):
    for blogger in bloggers:
        texts = []
        markdown_content = ""
        blogger_id = bloggers[blogger]
        for i in range(1, int(page)+1):
            url = bloggers_url.format(blogger_id, i)
            response = requests.get(url, headers=headers, cookies=cookies)
            data = response.json()
            try:
                # 提取发言内容并进行处理
                for item in data["statuses"]:
                    text = item["text"]
                    description = item["description"]
                    target = "xueqiu.com" + str(item["target"])
                    t = str(item['created_at'])
                    dt = datetime.fromtimestamp(int(t)/1000) # 将时间戳转换为datetime对象
                    formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S')
                    if commit_time < formatted_time:
                        if len(text) > 2:
                            texts.append(f"{formatted_time}:{text}\n[{target}]({target})")
                        else:
                            texts.append(f"{formatted_time}:{description}\n[{target}]({target})")
            except KeyError:
                print(blogger)

        # 在目录不存在时创建该目录，如果目录已经存在，则不会执行任何操作。
        directory = '../../CSV/xueqiu/Bloggers/{0}'.format(commit_time)
        os.makedirs(directory, exist_ok=True)

        # 定义Markdown文件名
        bloggers_file = "../../CSV/xueqiu/Bloggers/{2}/{0}{1}.md".format(blogger, commit_time, commit_time)

        # 将结果转换为Markdown格式
        markdown_content = "### {}\n\n".format(blogger+commit_time)
        markdown_content += "\n*********************************************************************************\n".join(
            texts)

        # write to markdown
        with open(bloggers_file, "w", encoding="utf-8") as file:
            file.write(markdown_content)

get_bloggers_status(bloggers=bloggers, commit_time='2024-03-29', page=1)
