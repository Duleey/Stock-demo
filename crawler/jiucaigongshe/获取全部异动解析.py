#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/27 3:49 下午
# @Author  : jianwei.lv

import requests
def getRes(date='2023-05-27'):
    cookies = {
        'SESSION': 'MzZkMTUwZjItNDkxZS00MzljLTg2NDYtOWU5ZmI5MGFjZDJl',
        'Hm_lvt_58aa18061df7855800f2a1b32d6da7f4': '1684118309',
        'UM_distinctid': '1881d460b2abea-0c50716c2d2f99-1d525634-1fa400-1881d460b2bfa4',
        'Hm_lpvt_58aa18061df7855800f2a1b32d6da7f4': '1686568302',
    }

    headers = {
        'authority': 'app.jiuyangongshe.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        # Already added when you pass json=
        # 'content-type': 'application/json',
        # 'cookie': 'SESSION=MzZkMTUwZjItNDkxZS00MzljLTg2NDYtOWU5ZmI5MGFjZDJl; Hm_lvt_58aa18061df7855800f2a1b32d6da7f4=1684118309; UM_distinctid=1881d460b2abea-0c50716c2d2f99-1d525634-1fa400-1881d460b2bfa4; Hm_lpvt_58aa18061df7855800f2a1b32d6da7f4=1686568302',
        'origin': 'https://www.jiuyangongshe.com',
        'platform': '3',
        'referer': 'https://www.jiuyangongshe.com/',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'timestamp': '1686568302295',
        'token': '629180b2a9e1b4a1217211952de797c3',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    }

    json_data = {
        'date': date,
        'pc': 1,
    }

    response = requests.post(
        'https://app.jiuyangongshe.com/jystock-app/api/v1/action/field',
        cookies=cookies,
        headers=headers,
        json=json_data,
    )

    return response

date = '2023-06-12'
file_path = f'../../CSV/jiucaigongshe/ydjx/{date}.md'

res = getRes(date=date)
for v in res.json()['data']:
    if 'list' in v:
        title_name = v['name']
        for l in v['list']:
            code = l['code']
            stock_name = l['name']
            expound = l['article']['action_info']['expound']

            # 打开一个新文件进行写入
            with open(file_path, "a") as f:
                # 将变量写入文件
                f.write(f"## {title_name}\n\n")
                f.write(f"###代码: {code}\n\n")
                f.write(f"股票名称: {stock_name}\n\n")
                f.write(f"解释: {expound}\n\n")
    else:
        date = v['date']
        with open(file_path, "a") as f:
            # 将变量写入文件
            f.write(f"# {date}\n\n")
