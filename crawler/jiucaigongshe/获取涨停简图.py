#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/27 3:22 下午
# @Author  : jianwei.lv

import requests
def get_res(date = '2023-05-26'):
    cookies = {
        'SESSION': 'MzZkMTUwZjItNDkxZS00MzljLTg2NDYtOWU5ZmI5MGFjZDJl',
        'Hm_lvt_58aa18061df7855800f2a1b32d6da7f4': '1684118309',
        'UM_distinctid': '1881d460b2abea-0c50716c2d2f99-1d525634-1fa400-1881d460b2bfa4',
        'Hm_lpvt_58aa18061df7855800f2a1b32d6da7f4': '1685172071',
    }

    headers = {
        'authority': 'app.jiuyangongshe.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        # 'cookie': 'SESSION=MzZkMTUwZjItNDkxZS00MzljLTg2NDYtOWU5ZmI5MGFjZDJl; Hm_lvt_58aa18061df7855800f2a1b32d6da7f4=1684118309; UM_distinctid=1881d460b2abea-0c50716c2d2f99-1d525634-1fa400-1881d460b2bfa4; Hm_lpvt_58aa18061df7855800f2a1b32d6da7f4=1685172071',
        'origin': 'https://www.jiuyangongshe.com',
        'platform': '3',
        'referer': 'https://www.jiuyangongshe.com/',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'timestamp': '1685173083006',
        'token': '92f92cc802d1a4890eeef9935074c6f5',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    }

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


date = '2023-05-26'
file_path = f'../../CSV/jiucaigongshe/ztjt/{date}'

res = get_res(date)
data = res.json()['data']
print(data)

res = requests.get(data)

# 将文件保存到本地
with open(file_path, 'wb') as f:
    f.write(res.content)