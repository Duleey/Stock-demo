#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/27 3:22 下午
# @Author  : jianwei.lv

import requests
import os

def get_res(date = '2023-05-26'):
    cookies = {
        'SESSION': 'OTFiNmJhYTQtNWM3Yy00M2E4LWI5ZDUtNWVhYWYxYThmN2Mx',
        'UM_distinctid': '18bc7f5670e34b-0ca1b3b473d9a1-17525634-168000-18bc7f5670f83f',
        'Hm_lvt_58aa18061df7855800f2a1b32d6da7f4': '1703551438,1704533688,1704801285',
        'Hm_lpvt_58aa18061df7855800f2a1b32d6da7f4': '1705222985',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        # Already added when you pass json=
        # 'Content-Type': 'application/json',
        # 'Cookie': 'SESSION=OTFiNmJhYTQtNWM3Yy00M2E4LWI5ZDUtNWVhYWYxYThmN2Mx; UM_distinctid=18bc7f5670e34b-0ca1b3b473d9a1-17525634-168000-18bc7f5670f83f; Hm_lvt_58aa18061df7855800f2a1b32d6da7f4=1703551438,1704533688,1704801285; Hm_lpvt_58aa18061df7855800f2a1b32d6da7f4=1705222985',
        'Origin': 'https://www.jiuyangongshe.com',
        'Referer': 'https://www.jiuyangongshe.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'platform': '3',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'timestamp': '1705223025933',
        'token': '00c9cca6bd143ed8dd702cd446499258',
    }

    # 在目录不存在时创建该目录，如果目录已经存在，则不会执行任何操作。
    directory = f'../../CSV/jiucaigongshe/ztjt/{date}'
    os.makedirs(directory, exist_ok=True)

    json_data = {
        'date': date,
    }

    response = requests.post(
        'https://app.jiuyangongshe.com/jystock-app/api/v1/action/diagram-url',
        cookies=cookies,
        headers=headers,
        json=json_data,
    )
    return response


date = '2023-01-10'
file_path = f'../../CSV/jiucaigongshe/ztjt/{date}/{date}.jpg'

res = get_res(date)
data = res.json()['data']
print(data)

res = requests.get(data)

# 将文件保存到本地
with open(file_path, 'wb') as f:
    f.write(res.content)