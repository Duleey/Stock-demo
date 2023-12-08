#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/27 3:49 下午
# @Author  : jianwei.lv

import numpy as np
import requests
import pandas as pd
import matplotlib.pyplot as plt
import os

def getRes(date='2023-07-28'):
    cookies = {
        'SESSION': 'MmU4NjMxM2EtZDY2Yy00ZDEyLThhYjMtOGM4NDdlN2MxZWFi',
        'UM_distinctid': '18bc7f5670e34b-0ca1b3b473d9a1-17525634-168000-18bc7f5670f83f',
        'Hm_lvt_58aa18061df7855800f2a1b32d6da7f4': '1699866830,1701078478,1702021135',
        'Hm_lpvt_58aa18061df7855800f2a1b32d6da7f4': '1702027138',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'SESSION=MmU4NjMxM2EtZDY2Yy00ZDEyLThhYjMtOGM4NDdlN2MxZWFi; UM_distinctid=18bc7f5670e34b-0ca1b3b473d9a1-17525634-168000-18bc7f5670f83f; Hm_lvt_58aa18061df7855800f2a1b32d6da7f4=1699866830,1701078478,1702021135; Hm_lpvt_58aa18061df7855800f2a1b32d6da7f4=1702027138',
        'Origin': 'https://www.jiuyangongshe.com',
        'Referer': 'https://www.jiuyangongshe.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'platform': '3',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'timestamp': '1702027138372',
        'token': 'ec3b573c4a2d8ac91f9fadb2c026b17f',
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

def csv_to_png(csv_path,title_name,date):
    # csv转图片
    # 读取CSV文件
    df = pd.read_csv(csv_path)

    # 每批数据的大小
    batch_size = 30

    # 数据总行数
    total_rows = len(df)

    # 计算需要分成多少批次
    num_batches = total_rows // batch_size + 1

    # 创建一个空白的图表
    fig, axs = plt.subplots(num_batches, 1, figsize=(3, 15))

    # Flatten the axs array using numpy
    axs_flat = np.ravel(axs)

    # Iterate through the flattened array
    for ax in axs_flat:
        ax.axis('off')

    try:
        # 遍历每个批次
        for i in range(num_batches):
            start_index = i * batch_size
            end_index = min((i + 1) * batch_size, total_rows)
            batch_data = df.values[start_index:end_index]
            # print(f"Batch {i + 1} data: {batch_data}")

            # 为每个批次创建一个新的子图
            ax = fig.add_subplot(num_batches, 1, i+1)
            ax.axis('off')

            # 在子图中创建表格
            table = ax.table(cellText=batch_data, colLabels=df.columns, loc='center')

            # 设置表格样式
            table.auto_set_font_size(False)
            table.set_fontsize(10)
            table.scale(1.2, 1.2)

            # 将子图保存为图片
            batch_pic_path = f'../../CSV/jiucaigongshe/ydjx/{date}/{title_name}{date}_batch{i + 1}.png'
            plt.savefig(batch_pic_path)

            # 清除子图内容
            table.remove()

        # 关闭图表
        plt.close()
    except IndexError:
        print(IndexError)


date = '2023-12-08'
file_path = f'../../CSV/jiucaigongshe/ydjx/{date}/{date}.md'
csv_path = f'../../CSV/jiucaigongshe/ydjx/{date}/{date}.csv'
pic_path = f'../../CSV/jiucaigongshe/ydjx/{date}/{date}.png'
res = getRes(date=date)

title_check = "check"

# 在目录不存在时创建该目录，如果目录已经存在，则不会执行任何操作。
directory = f'../../CSV/jiucaigongshe/ydjx/{date}'
os.makedirs(directory, exist_ok=True)

for v in res.json()['data']:
    if 'list' in v:
        if '/' in v['name']:
            store = v['name'].replace("/", "&")
            v['name'] = store
        title_name = v['name']
        for l in v['list']:
            code = l['code']
            stock_name = l['name']
            time = l['article']['action_info']['time']
            if time == '':
                time = '没有涨停'
            expound = l['article']['action_info']['expound']

            # 依次比对，提取每个大类并存入md
            if title_name != title_check:
                title_check = title_name

            with open(f'../../CSV/jiucaigongshe/ydjx/{date}/{title_check}{date}.md', "a+") as f:
                # if code[:2] == 'bj':
                #     code = code[2:]
                # 将变量写入文件
                f.write(f"## {title_name}\n\n")
                f.write(f"###代码: {code}\n\n")
                f.write(f"股票名称: {stock_name}\n\n")
                f.write(f"涨停时间: {time}\n\n")
                f.write(f"解释: {expound}\n\n")

            with open(f'../../CSV/jiucaigongshe/ydjx/{date}/{title_check}{date}.csv', "a") as f:
                f.write(f"{code}\n\n")

            csv_to_png(csv_path=f'../../CSV/jiucaigongshe/ydjx/{date}/{title_check}{date}.csv',
                       title_name=title_check,
                       date=date)

            # 将所有类型写入一个文件
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

csv_to_png(csv_path=csv_path, title_name="所有", date=date)

