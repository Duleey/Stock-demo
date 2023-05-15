#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/13 10:15 下午
# @Author  : jianwei.lv

import requests
from bs4 import BeautifulSoup

# 关注的博主用户名列表
bloggers = ["8940371568"]

# 关注的组合列表
portfolios = ["portfolio1", "portfolio2", "portfolio3"]

# 发言提示URL
bloggers_url = "https://xueqiu.com/v4/statuses/user_timeline.json?user_id={}&page=1"

# 调仓提示URL
portfolios_url = "https://xueqiu.com/P/ZH1067274"

# 请求头信息
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
    "Cookie": "device_id=b113b3700ba6f60d2c110d9a9374ab5a; s=c81992ym9d; bid=f2482796a6eda57a039c2760d1448818_lfgoelhg; Hm_lvt_1db88642e346389874251b5a1eded6e3=1681639310,1681692930,1681693130,1681779457; snbim_minify=true; remember=1; xq_a_token=13d4c4747887c96b540faf6f35d64f5aaaa1c838; xqat=13d4c4747887c96b540faf6f35d64f5aaaa1c838; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjMwNTgxOTA4MzEsImlzcyI6InVjIiwiZXhwIjoxNjg2NjY0NDY1LCJjdG0iOjE2ODQxMTE3MDg5MjEsImNpZCI6ImQ5ZDBuNEFadXAifQ.l1P8Oastt5csWhmNUR_-DmDg7rzr6A9WbkToUK33YNmeAu0mixLNFtpxY7Eir8hl4AfG7nrbYEMRbAXNsJYQ9qUMZsrP0MK6xgpv8x15DdQ0tMdB8aftT9xR0VO3BfwNKzg9JteyZUnrVt1yXp6x15vbRUNJ-_XjZPpJ5LkkVTqxWyY_t8JrDGq-Iog6bSZgboOjE8ocpW_Qa4hmR0DY5FFBZ4-M__7UwkvnSGh1GS6N9vE3KgHc3PVjxqZDBPq4qa3A6BVDXPb0cWFal9VnmqADlBNTNmfzu1uhA6j7lWYjB8TBF-WHhRREiKeCRjF2B-uGLge9X0UjgonwzvcWHA; xq_r_token=2656a2c4a38efe137c5821e5e9e963d206ca2b01; xq_is_login=1; u=3058190831; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1684144548; is_overseas=1"
}

def get_bloggers_status(bloggers):
    for blogger in bloggers:
        url = bloggers_url.format(blogger)
        response = requests.get(url, headers=headers)
        data = response.json()

        # 提取发言内容并进行处理
        for item in data["statuses"]:
            status_id = item["id"]
            text = item["text"]
            description=item["description"]
            # 在这里可以添加自定义的处理逻辑，例如发送通知等
            return description

def get_portfolios_insights(portfolios):
    response = requests.get(portfolios_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # 提取调仓提示内容并进行处理
    insights = soup.select(".table__insight-content")
    for insight in insights:
        text = insight.get_text()
        # 在这里可以添加自定义的处理逻辑，例如发送通知等
        return text

# 调用函数进行监控
res=get_bloggers_status(bloggers)
res1=get_portfolios_insights(portfolios)
print(res)
print(res1)
