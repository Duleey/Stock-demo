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
    "投研家": "8940371568",
    "万得调研": "4198802945",
    "雪月霜": "1505944393",
    "飞鱼说周期": "8780715730",
    "投研与逻辑": "2852344450",
    "寒山invest": "5441610555",
    "雷雨季节": "1072107809"
}

# 发言提示URL
bloggers_url = "https://xueqiu.com/v4/statuses/user_timeline.json?user_id={0}&page={1}"

# 请求头信息
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
    "Cookie": "device_id=b113b3700ba6f60d2c110d9a9374ab5a; s=c81992ym9d; bid=f2482796a6eda57a039c2760d1448818_lfgoelhg; __utmz=1.1679307632.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); snbim_minify=true; __utmc=1; Hm_lvt_1db88642e346389874251b5a1eded6e3=1684372633; __utma=1.1859006477.1679307632.1684911389.1685096759.49; acw_tc=2760827816854073512595151ec395e513836a41f0153c92a42ad874b9661c; remember=1; xq_a_token=774979a51aed8fc0644a9b73cae8ae612d304c76; xqat=774979a51aed8fc0644a9b73cae8ae612d304c76; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjMwNTgxOTA4MzEsImlzcyI6InVjIiwiZXhwIjoxNjg3OTYxNzMzLCJjdG0iOjE2ODU0MDg1NDg0MTYsImNpZCI6ImQ5ZDBuNEFadXAifQ.hMh1xGnHA2cxZYpFt53n0imZpYZSU7pgqDh-p-GDN7wwbvgXgiIDRc5YJtdpMMTUsBnJxql9VKszFeD7sB3UoyaWJGN62F78F1UGsUFZ9TgNrRtzdnE1250Jm2eLOsSN5LpqtgS7_O9WKkjpMEDVxwBV-Bj9LRmdAxPwZtUz7dOmvODhXc67BHNEqLbGRu4vwLgjYEkyJinKro6la2J_3-pwy4-UU3WfmEfXaUXYZU-ZmezkJdntU0ArOjvtkWAJfUsTGaJXRl_LyNB7NQ9YSVO8GIFp4cc9dMMhIQHbtZmyA05WP8ozj3gha6pXN7HAoLVM_QcR5B8j3VOXglRMjA; xq_r_token=af5076fc5f21d8691bd4657a2a242249b97a76d3; xq_is_login=1; u=3058190831; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1685408675"
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

get_bloggers_status(bloggers=bloggers, commit_time='2023-06-12', page=1)
