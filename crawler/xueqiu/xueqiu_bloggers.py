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
    "神猫识顶底": "8350226665"
}

# 发言提示URL
bloggers_url = "https://xueqiu.com/v4/statuses/user_timeline.json?user_id={0}&page={1}"

# 请求头信息

cookies = {
    'device_id': 'b113b3700ba6f60d2c110d9a9374ab5a',
    's': 'c81992ym9d',
    'bid': 'f2482796a6eda57a039c2760d1448818_lfgoelhg',
    'cookiesu': '251692352267798',
    'u': '3058190831',
    'xq_is_login': '1',
    'snbim_minify': 'true',
    'Hm_lvt_1db88642e346389874251b5a1eded6e3': '1708757682',
    'xq_a_token': 'd54d1258c491f7059fd0520facd26feda026c390',
    'xqat': 'd54d1258c491f7059fd0520facd26feda026c390',
    'xq_id_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjMwNTgxOTA4MzEsImlzcyI6InVjIiwiZXhwIjoxNzEyNDY5MjY3LCJjdG0iOjE3MDk4NzcyNjc1MDEsImNpZCI6ImQ5ZDBuNEFadXAifQ.kMUKxPfQ9o5JyB1HhgsVxKJg0MY2mxKdjEyIlsqFN93OfWBmogM8nwXfsWZ5f4QeO9ZlRhQOHoGUnD9EqeqQ0tDPVJ6CXamYTEMPZGl7Ho8GbDOCl1XCg2Jo327aONwlVla0YbT_GOLVFE-XhMXZKK5kb2RfwI-R2lEzyY-kOETolY962Qr8wyapHoZRp2235t4u8Cwa7l0binfcjs6GbNR7oOBvjKsgrQhlVV4WFmtMghCHYbOV2SDvuu95weey-u0AjFMa7dvPKSGbVMSJOsJiCzeMtSIPuCcCxeknDyhT_Y0kFEAr8VT3xrnU3C--5GzpYDTQC400j3KJvLYKXw',
    'xq_r_token': '373cfdad2c783ec3da34526661f1d911126ba341',
    'is_overseas': '0',
    'Hm_lpvt_1db88642e346389874251b5a1eded6e3': '1710224109',
}

headers = {
    'authority': 'stock.xueqiu.com',
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    # 'cookie': 'device_id=b113b3700ba6f60d2c110d9a9374ab5a; s=c81992ym9d; bid=f2482796a6eda57a039c2760d1448818_lfgoelhg; cookiesu=251692352267798; u=3058190831; xq_is_login=1; snbim_minify=true; Hm_lvt_1db88642e346389874251b5a1eded6e3=1708757682; xq_a_token=d54d1258c491f7059fd0520facd26feda026c390; xqat=d54d1258c491f7059fd0520facd26feda026c390; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjMwNTgxOTA4MzEsImlzcyI6InVjIiwiZXhwIjoxNzEyNDY5MjY3LCJjdG0iOjE3MDk4NzcyNjc1MDEsImNpZCI6ImQ5ZDBuNEFadXAifQ.kMUKxPfQ9o5JyB1HhgsVxKJg0MY2mxKdjEyIlsqFN93OfWBmogM8nwXfsWZ5f4QeO9ZlRhQOHoGUnD9EqeqQ0tDPVJ6CXamYTEMPZGl7Ho8GbDOCl1XCg2Jo327aONwlVla0YbT_GOLVFE-XhMXZKK5kb2RfwI-R2lEzyY-kOETolY962Qr8wyapHoZRp2235t4u8Cwa7l0binfcjs6GbNR7oOBvjKsgrQhlVV4WFmtMghCHYbOV2SDvuu95weey-u0AjFMa7dvPKSGbVMSJOsJiCzeMtSIPuCcCxeknDyhT_Y0kFEAr8VT3xrnU3C--5GzpYDTQC400j3KJvLYKXw; xq_r_token=373cfdad2c783ec3da34526661f1d911126ba341; is_overseas=0; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1710224109',
    'origin': 'https://xueqiu.com',
    'referer': 'https://xueqiu.com/',
    'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
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

get_bloggers_status(bloggers=bloggers, commit_time='2024-03-12', page=1)
