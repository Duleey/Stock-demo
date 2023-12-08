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
    "十年七倍": "9821253825",
    "周期合伙人": "6347482150",
    "UESTC独钓寒江雪": "2377563498",
    "密探一号": "9999782882",
    "三生万物时": "1695241710",
    "洒脱的古龙": "7977236763",
    "斯卡纳贝": "3352558222",
    "乘黄18": "3945042689",
    "银河投递员": "1718809686",
    "双子窥天新号": "3849856324",
    "鲨鱼哥的视频逻辑": "7447535920",
    "无心0000": "250386640",
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
    "好习惯受用终生": "4015596010"
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
    'snbim_minify': 'true',
    'Hm_lvt_1db88642e346389874251b5a1eded6e3': '1700699665',
    'remember': '1',
    'xq_a_token': 'dddc9b5bd16cbc95abcd82c3bc71d83fe7ca62ec',
    'xqat': 'dddc9b5bd16cbc95abcd82c3bc71d83fe7ca62ec',
    'xq_id_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjMwNTgxOTA4MzEsImlzcyI6InVjIiwiZXhwIjoxNzAzODYyNDA2LCJjdG0iOjE3MDEzOTE3MjA4MDgsImNpZCI6ImQ5ZDBuNEFadXAifQ.jGdjTHxFFUQ5dkWOThoX2qTMCP9hI9n-mjKutUGa_iRPI8cLJCkugD69gs5v_T92iokJe2tPU6f6xdlHmexyCbVopT-UvX54I7TS7OWBk3CRFS34kY1l78pEfo0tKADp3abWgGqf8mb8ooW5dZo9XgSqSDjDYlmOypQ9FkLaaDazCKUiPe5uDQKpllS4gED2z9EJUhicH_0QZqvytGInhAtRcGaYc6Mv0r3OHwpItYBvqTSZOvhLq4MF-sG2F5Bk0lveSDDNowz3_D6L0kD32tqbgpOfttZOTqLmv6iphw9X1WeWXqOS-kL-kiXIi8zQ3tPtZOOM7KlR8V7JdHH69A',
    'xq_r_token': '299f3b472218c80e451f65212a32220bc11bfaa4',
    'xq_is_login': '1',
    'Hm_lpvt_1db88642e346389874251b5a1eded6e3': '1701677658',
    'acw_tc': '0bd17c4a17016806424312082ed76a6de460e9a25e1ef7596eddc6c393253c',
    'is_overseas': '0',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    # 'Cookie': 'device_id=b113b3700ba6f60d2c110d9a9374ab5a; s=c81992ym9d; bid=f2482796a6eda57a039c2760d1448818_lfgoelhg; cookiesu=251692352267798; u=3058190831; snbim_minify=true; Hm_lvt_1db88642e346389874251b5a1eded6e3=1700699665; remember=1; xq_a_token=dddc9b5bd16cbc95abcd82c3bc71d83fe7ca62ec; xqat=dddc9b5bd16cbc95abcd82c3bc71d83fe7ca62ec; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjMwNTgxOTA4MzEsImlzcyI6InVjIiwiZXhwIjoxNzAzODYyNDA2LCJjdG0iOjE3MDEzOTE3MjA4MDgsImNpZCI6ImQ5ZDBuNEFadXAifQ.jGdjTHxFFUQ5dkWOThoX2qTMCP9hI9n-mjKutUGa_iRPI8cLJCkugD69gs5v_T92iokJe2tPU6f6xdlHmexyCbVopT-UvX54I7TS7OWBk3CRFS34kY1l78pEfo0tKADp3abWgGqf8mb8ooW5dZo9XgSqSDjDYlmOypQ9FkLaaDazCKUiPe5uDQKpllS4gED2z9EJUhicH_0QZqvytGInhAtRcGaYc6Mv0r3OHwpItYBvqTSZOvhLq4MF-sG2F5Bk0lveSDDNowz3_D6L0kD32tqbgpOfttZOTqLmv6iphw9X1WeWXqOS-kL-kiXIi8zQ3tPtZOOM7KlR8V7JdHH69A; xq_r_token=299f3b472218c80e451f65212a32220bc11bfaa4; xq_is_login=1; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1701677658; acw_tc=0bd17c4a17016806424312082ed76a6de460e9a25e1ef7596eddc6c393253c; is_overseas=0',
    'Origin': 'https://xueqiu.com',
    'Referer': 'https://xueqiu.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
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
        directory = f'../../CSV/xueqiu/Bloggers/{0}'.format(commit_time)
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

get_bloggers_status(bloggers=bloggers, commit_time='2023-12-08', page=1)
