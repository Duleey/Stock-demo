#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/27 3:49 下午
# @Author  : jianwei.lv

import requests
import pandas as pd
import matplotlib.pyplot as plt

def getRes(date='2023-07-28'):
    cookies = {
        'UM_distinctid': '1881d460b2abea-0c50716c2d2f99-1d525634-1fa400-1881d460b2bfa4',
        'Hm_lvt_58aa18061df7855800f2a1b32d6da7f4': '1692837497,1693643715',
        'Hm_lpvt_58aa18061df7855800f2a1b32d6da7f4': '1694501687',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'SESSION=M2NiMTVhYmItZDNhMy00M2Q1LTk2Y2EtNDMxZjk3ODhkNmU1; Hm_lvt_58aa18061df7855800f2a1b32d6da7f4=1697763060',
        'Origin': 'https://www.jiuyangongshe.com',
        'Referer': 'https://www.jiuyangongshe.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'platform': '3',
        'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'timestamp': '1699866755415',
        'token': 'd6b5dc276fb121d14ae97fb091ce1f1c',
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

date = '2023-11-13'
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

# 每批数据的大小
batch_size = 50

# 数据总行数
total_rows = len(df)

# 计算需要分成多少批次
num_batches = total_rows // batch_size + 1

# 创建一个空白的图表
fig, axs = plt.subplots(num_batches, 1, figsize=(3, 15))

# 隐藏坐标轴
for ax in axs:
    ax.axis('off')

# 分批创建表格并填充数据
for i in range(num_batches):
    start_index = i * batch_size
    end_index = min((i + 1) * batch_size, total_rows)
    batch_data = df.values[start_index:end_index]
    print(batch_data)
    print(len(batch_data))
    print('-----------------')

    # 在对应的子图表中创建表格
    table = axs[i].table(cellText=batch_data, colLabels=df.columns, loc='center')

    # 设置表格样式
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)

    # 保存图表为图片
    batch_pic_path = f'../../CSV/jiucaigongshe/ydjx/{date}_batch{i + 1}.png'
    plt.savefig(batch_pic_path)

    # 清除图表内容
    table.remove()

# 关闭图表
plt.close()

# 显示图表
plt.show()