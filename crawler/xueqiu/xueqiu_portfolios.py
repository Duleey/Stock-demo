#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/17 11:32 上午
# @Author  : jianwei.lv

import requests
import json
from datetime import datetime

# 关注的组合列表 https://xueqiu.com/P/ZH1067274
portfolios = {"ZH1067274": {
    "rb_id": "138890721",
    "cube_symbol": "ZH1067274"
}}

# 调仓提示URL
portfolios_url = "https://xueqiu.com/cubes/rebalancing/show_origin.json?rb_id={0}&cube_symbol={1}"

# 请求头信息
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
    "Cookie": "device_id=b113b3700ba6f60d2c110d9a9374ab5a; s=c81992ym9d; bid=f2482796a6eda57a039c2760d1448818_lfgoelhg; Hm_lvt_1db88642e346389874251b5a1eded6e3=1681639310,1681692930,1681693130,1681779457; snbim_minify=true; remember=1; xq_a_token=13d4c4747887c96b540faf6f35d64f5aaaa1c838; xqat=13d4c4747887c96b540faf6f35d64f5aaaa1c838; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjMwNTgxOTA4MzEsImlzcyI6InVjIiwiZXhwIjoxNjg2NjY0NDY1LCJjdG0iOjE2ODQxMTE3MDg5MjEsImNpZCI6ImQ5ZDBuNEFadXAifQ.l1P8Oastt5csWhmNUR_-DmDg7rzr6A9WbkToUK33YNmeAu0mixLNFtpxY7Eir8hl4AfG7nrbYEMRbAXNsJYQ9qUMZsrP0MK6xgpv8x15DdQ0tMdB8aftT9xR0VO3BfwNKzg9JteyZUnrVt1yXp6x15vbRUNJ-_XjZPpJ5LkkVTqxWyY_t8JrDGq-Iog6bSZgboOjE8ocpW_Qa4hmR0DY5FFBZ4-M__7UwkvnSGh1GS6N9vE3KgHc3PVjxqZDBPq4qa3A6BVDXPb0cWFal9VnmqADlBNTNmfzu1uhA6j7lWYjB8TBF-WHhRREiKeCRjF2B-uGLge9X0UjgonwzvcWHA; xq_r_token=2656a2c4a38efe137c5821e5e9e963d206ca2b01; xq_is_login=1; u=3058190831; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1684144548; is_overseas=1"
}

def get_portfolios(portfolios):
    for portfolio in portfolios:
        url = portfolios_url.format(portfolios[portfolio]["rb_id"], portfolios[portfolio]["cube_symbol"])
        response = requests.get(url, headers=headers)
        data = response.json()

        # 提取发言内容并进行处理
        results = []
        for item in data["rebalancing"]["rebalancing_histories"]:
            id = item["id"]
            rebalancing_id = item["id"]
            stock_id = item["stock_id"]
            stock_name = item["stock_name"]
            stock_symbol = item["stock_symbol"]
            price = item["price"]
            weight = item["weight"]
            prev_weight = item["prev_weight"]

            # 将每个 portfolio 转换为一个字典
            portfolio_dict = {
                "id": id,
                "rebalancing_id": rebalancing_id,
                "stock_id": stock_id,
                "stock_name": stock_name,
                "stock_symbol": stock_symbol,
                "price": price,
                "weight": weight,
                "prev_weight": prev_weight
            }

            # 将字典添加到结果列表中
            results.append(portfolio_dict)
            # 将结果列表转换为 JSON 格式
        return json.dumps(results)


# 调用函数进行监控
res1 = get_portfolios(portfolios)

# 定义Markdown文件名
bloggers_file = "../CSV/bloggers.md"
portfolios_file = "../CSV/portfolios.md"

def write_to_markdown(file_name, content):
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(content)

# 调用函数进行监控
res1 = get_portfolios(portfolios)

# 定义Markdown文件名
portfolios_file = "../CSV/portfolios.md"

def write_to_markdown(file_name, content):
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(content)


# 将结果转换为Markdown格式
markdown_content = "### Portfolios\n\n"
markdown_content += res1
write_to_markdown(portfolios_file, markdown_content)