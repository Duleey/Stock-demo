#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/27 3:49 下午
# @Author  : jianwei.lv

import requests
import pandas as pd
import matplotlib.pyplot as plt

def getRes(date='2023-07-28'):
    cookies = {
        'SESSION': 'OTI0YWZmZDMtNTE4OC00Y2M2LTkyYzYtZWIzNTcyMWVlYWI4',
        'UM_distinctid': '1881d460b2abea-0c50716c2d2f99-1d525634-1fa400-1881d460b2bfa4',
        'Hm_lvt_58aa18061df7855800f2a1b32d6da7f4': '1689133256,1689509248,1689555723',
        'Hm_lpvt_58aa18061df7855800f2a1b32d6da7f4': '1690538250',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        # Already added when you pass json=
        # 'Content-Type': 'application/json',
        # 'Cookie': 'SESSION=OTI0YWZmZDMtNTE4OC00Y2M2LTkyYzYtZWIzNTcyMWVlYWI4; UM_distinctid=1881d460b2abea-0c50716c2d2f99-1d525634-1fa400-1881d460b2bfa4; Hm_lvt_58aa18061df7855800f2a1b32d6da7f4=1689133256,1689509248,1689555723; Hm_lpvt_58aa18061df7855800f2a1b32d6da7f4=1690882750',
        'Origin': 'https://www.jiuyangongshe.com',
        'Referer': 'https://www.jiuyangongshe.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'platform': '3',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'timestamp': '1690882750191',
        'token': 'd999e3a241b92ea963b6c65202226240',
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

date = '2023-08-03'
file_path = f'../../CSV/jiucaigongshe/ydjx/{date}.md'
csv_path = f'../../CSV/jiucaigongshe/ydjx/{date}.csv'
pic_path = f'../../CSV/jiucaigongshe/ydjx/{date}.png'
res = getRes(date=date)
for v in res.json()['data']:
    if 'list' in v:
        title_name = v['name']
        for l in v['list']:
            code = l['code']
            stock_name = l['name']
            time = l['article']['action_info']['time']
            if time == '':
                time = '没有涨停'
            expound = l['article']['action_info']['expound']

            # 打开一个新文件进行写入
            with open(file_path, "a") as f:
                # 将变量写入文件
                f.write(f"## {title_name}\n\n")
                f.write(f"###代码: {code}\n\n")
                f.write(f"股票名称: {stock_name}\n\n")
                f.write(f"涨停时间: {time}\n\n")
                f.write(f"解释: {expound}\n\n")

            # 导入一份csv,只有代码
            with open(csv_path, "a") as f:
                f.write(f"{code}\n\n")
    else:
        date = v['date']
        with open(file_path, "a") as f:
            # 将变量写入文件
            f.write(f"# {date}\n\n")

# csv转图片
# 读取CSV文件
df = pd.read_csv(csv_path)

# 创建一个空白的图表
fig, ax = plt.subplots(figsize=(3, 25))

# 隐藏坐标轴
ax.axis('off')

# 创建表格并填充数据
table = ax.table(cellText=df.values, colLabels=df.columns, loc='center')

# 设置表格样式
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 1.2)

# 保存图表为图片
plt.savefig(pic_path)

# 显示图表
plt.show()