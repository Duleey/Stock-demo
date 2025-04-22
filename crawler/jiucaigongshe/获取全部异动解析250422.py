import numpy as np
import requests
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

def getRes(date='2023-07-28'):
    cookies = {
        'SESSION': 'MGQ2YTA2MjAtNTdkYy00Y2NjLWJhZTEtYjMyMGE2ZDFhNGJi',
        'Hm_lvt_58aa18061df7855800f2a1b32d6da7f4': '1743516596,1744114637,1745236931,1745323955',
        'Hm_lpvt_58aa18061df7855800f2a1b32d6da7f4': '1745323955',
    }

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://www.jiuyangongshe.com',
        'platform': '3',
        'priority': 'u=1, i',
        'referer': 'https://www.jiuyangongshe.com/',
        'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'timestamp': '1745323961673',
        'token': '2fb312c6f3db45abbc3adf1b014bdd45',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
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

def csv_to_png(csv_path, title_name, date):
    """将 CSV 数据转为 PNG 图片"""
    try:
        df = pd.read_csv(csv_path, header=None)  # 假设 CSV 没有表头
    except pd.errors.EmptyDataError:
        print(f"⚠️ CSV 文件为空: {csv_path}")
        return
    except FileNotFoundError:
        print(f"❌ 文件未找到: {csv_path}")
        return

    if df.empty:
        print(f"⚠️ 无数据可转换: {csv_path}")
        return

    batch_size = 30
    total_rows = len(df)
    num_batches = (total_rows // batch_size) + 1

    fig, axs = plt.subplots(num_batches, 1, figsize=(10, 5 * num_batches))
    if num_batches == 1:
        axs = [axs]  # 确保 axs 是列表

    for i, ax in enumerate(axs):
        start_idx = i * batch_size
        end_idx = min((i + 1) * batch_size, total_rows)
        batch_data = df.iloc[start_idx:end_idx]

        ax.axis('off')
        if i == 0:
            table = ax.table(
                cellText=batch_data.values,
                colLabels=df.columns,
                loc='center',
                cellLoc='center'
            )
        else:
            table = ax.table(
                cellText=batch_data.values,
                loc='center',
                cellLoc='center'
            )
        table.auto_set_font_size(False)
        table.set_fontsize(8)
        table.scale(1.2, 1.2)

    output_dir = os.path.dirname(csv_path)
    output_png = os.path.join(output_dir, f"{title_name}_{date}.png")
    try:
        plt.tight_layout()
        plt.savefig(output_png, bbox_inches='tight', dpi=150)
        plt.close()
        print(f"✅ 图片已保存: {output_png}")
    except Exception as e:
        print(f"❌ 保存图片时出错: {e}")

def main(date='2025-04-22'):
    res = getRes(date=date)
    if not res.ok:
        print(f"❌ 请求失败: HTTP {res.status_code}")
        return

    data = res.json().get('data', [])
    if not data:
        print(f"❌ 无数据返回，请检查日期: {date}")
        return

    # 创建存储目录
    output_dir = os.path.join(r'D:\workspace\量化\Stock-demo\CSV\jiucaigongshe\ydjx', date)
    try:
        os.makedirs(output_dir, exist_ok=True)
    except FileExistsError:
        pass
    except Exception as e:
        print(f"❌ 创建目录时出错: {e}")
        return

    # 主文件路径
    main_md_path = os.path.join(output_dir, f"{date}.md")
    main_csv_path = os.path.join(output_dir, f"{date}.csv")

    # 清空或创建主文件
    try:
        with open(main_md_path, 'w', encoding='utf-8') as f_main_md, \
             open(main_csv_path, 'w', encoding='utf-8') as f_main_csv:
            f_main_md.write(f"# {date}\n\n")
            f_main_csv.write("股票代码\n")  # CSV 表头
    except Exception as e:
        print(f"❌ 创建主文件时出错: {e}")
        return

    title_check = "check"

    for item in data:
        if 'list' not in item:
            continue

        title_name = item['name'].replace("/", "&")  # 处理特殊字符
        category_md_path = os.path.join(output_dir, f"{title_name}_{date}.md")
        category_csv_path = os.path.join(output_dir, f"{title_name}_{date}.csv")

        try:
            with open(category_md_path, 'w', encoding='utf-8') as f_category_md, \
                 open(category_csv_path, 'w', encoding='utf-8') as f_category_csv, \
                 open(main_md_path, 'a', encoding='utf-8') as f_main_md, \
                 open(main_csv_path, 'a', encoding='utf-8') as f_main_csv:

                f_category_md.write(f"## {title_name}\n\n")
                f_main_md.write(f"## {title_name}\n\n")

                for stock in item['list']:
                    code = stock['code']
                    name = stock['name']
                    time = stock['article']['action_info']['time'] or "没有涨停"
                    expound = stock['article']['action_info']['expound']

                    # 写入分类文件
                    f_category_md.write(f"### 代码: {code}\n\n股票名称: {name}\n\n涨停时间: {time}\n\n解释: {expound}\n\n")
                    f_category_csv.write(f"{code}\n")

                    # 写入主文件
                    f_main_md.write(f"### 代码: {code}\n\n股票名称: {name}\n\n涨停时间: {time}\n\n解释: {expound}\n\n")
                    f_main_csv.write(f"{code}\n")

                # 生成分类图片
                csv_to_png(category_csv_path, title_name, date)
        except Exception as e:
            print(f"❌ 处理 {title_name} 数据时出错: {e}")

    # 遍历目录下所有 CSV 文件并转换为 PNG
    for filename in os.listdir(output_dir):
        if filename.endswith('.csv'):
            title_name = os.path.splitext(filename)[0].replace(f"_{date}", "")
            csv_path = os.path.join(output_dir, filename)
            csv_to_png(csv_path, title_name, date)

    print(f"✅ 数据处理完成，目录: {output_dir}")

if __name__ == "__main__":
    main(date='2025-04-22')  # 可修改日期
