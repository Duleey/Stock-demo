#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/13 10:15 下午
# @Author  : jianwei.lv

import requests
from datetime import datetime
import time

# 关注的博主用户名列表 https://xueqiu.com/u/8940371568
# 博主名：id
bloggers = {
    # "投研家": "8940371568",
    # "万得调研": "4198802945",
    "雪月霜": "1505944393",
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
    "洒脱的古龙": "7977236763"
}

# 发言提示URL
bloggers_url = "https://xueqiu.com/v4/statuses/user_timeline.json?user_id={0}&page={1}"

# 请求头信息
headers = headers = {
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://xueqiu.com/',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'sec-ch-ua-platform': '"macOS"',
}

def get_bloggers_status(bloggers, commit_time, page=1):
    for blogger in bloggers:
        texts = []
        markdown_content = ""
        blogger_id = bloggers[blogger]
        for i in range(1, int(page)+1):
            url = bloggers_url.format(blogger_id, i)
            response = requests.get(url, headers=headers)
            data = response.json()

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

        # 定义Markdown文件名
        bloggers_file = "../CSV/xueqiu/Bloggers/{0}{1}.md".format(blogger, commit_time)

        # 将结果转换为Markdown格式
        markdown_content = "### {}\n\n".format(blogger+commit_time)
        markdown_content += "\n*********************************************************************************\n".join(
            texts)

        # write to markdown
        with open(bloggers_file, "w", encoding="utf-8") as file:
            file.write(markdown_content)

get_bloggers_status(bloggers=bloggers, commit_time='2023-08-03', page=1)
