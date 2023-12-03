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
    # "投研家": "8940371568",
    # "万得调研": "4198802945",
    # "雪月霜": "1505944393",
    "投研与逻辑": "2852344450",
    "寒山invest": "5441610555",
    "雷雨季节": "1072107809",
    "花盆君": "5452093377",
    "合理出奇迹": "1708120238",
    "十年七倍": "9821253825",
    "周期合伙人": "6347482150",
    "UESTC独钓寒江雪": "2377563498",
    "密探一号": "9999782882",
    "三生万物时": "1695241710",
    "洒脱的古龙": "7977236763",
    "斯卡纳贝": "3352558222",
    "乘黄18": "3945042689",
    "银河投递员": "1718809686",
    "双子窥天新号": "3849856324",
    "鲨鱼哥的视频逻辑": "7447535920",
    "无心0000": "250386640",
    "无鸣之辈-阿飞": "4253976756",
    "本股神": "1819336967",
    "轮回666": "8282709675",
    "疯狂梭哈哥": "8282709675",
    "rtu8": "2759777767"
}

# 发言提示URL
bloggers_url = "https://xueqiu.com/v4/statuses/user_timeline.json?user_id={0}&page={1}"

# 请求头信息
cookies = {
    'device_id': 'b113b3700ba6f60d2c110d9a9374ab5a',
    's': 'c81992ym9d',
    'bid': 'f2482796a6eda57a039c2760d1448818_lfgoelhg',
    '__utmz': '1.1679307632.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    'cookiesu': '251692352267798',
    'u': '3058190831',
    'xq_is_login': '1',
    'xq_a_token': '385c56b4e59770790d2247eafc862225acdb5ec8',
    'xqat': '385c56b4e59770790d2247eafc862225acdb5ec8',
    'xq_id_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjMwNTgxOTA4MzEsImlzcyI6InVjIiwiZXhwIjoxNzAyNTM5NTUyLCJjdG0iOjE2OTk5NDc1NTIxMTgsImNpZCI6ImQ5ZDBuNEFadXAifQ.XeViKuPpfkjZarNz-IUmhJ1jkOk5lSFc1v8dKB5hxL37JS7Xgb63EWDVghKjfPRAdW4iHCpikSCJFwa1-iC7RGBQfLjrQqO7NYIB-ZI8YlfcmxrhlDxNSMPgjcvZwYc6E_CxFopxHawN9zBfrLcAuZMFFQVQ2ooMZA2SIDBwgHBJJIktKmbwJueEcf7AdNvZw3x5vEe-KfLsBfcgnyffPpKvct4J8rVQNGXceQZ1SlS6cFZIg7e6CRErOyE7nl7yQPwrMqabQJdFhi-UNwekrNrjMqqH2opfQIMNcgYGvXAlQabOZ0u2P1bdg5xgDW06yAbR6UU_xH-qu49lKlDuxg',
    'xq_r_token': 'e582d7d935fe508a65c8967a588fb3c2acb8a4d3',
    '__utma': '1.1859006477.1679307632.1697616458.1700647838.84',
    'Hm_lvt_1db88642e346389874251b5a1eded6e3': '1698644247,1700699665',
    'acw_tc': '2760779117007242621364913eb7b2720911cf4a0eca0f126e2221064fae47',
    'is_overseas': '0',
    'Hm_lpvt_1db88642e346389874251b5a1eded6e3': '1700724265',
    'snbim_minify': 'true',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    # 'Cookie': 'device_id=b113b3700ba6f60d2c110d9a9374ab5a; s=c81992ym9d; bid=f2482796a6eda57a039c2760d1448818_lfgoelhg; __utmz=1.1679307632.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); cookiesu=251692352267798; u=3058190831; xq_is_login=1; xq_a_token=385c56b4e59770790d2247eafc862225acdb5ec8; xqat=385c56b4e59770790d2247eafc862225acdb5ec8; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjMwNTgxOTA4MzEsImlzcyI6InVjIiwiZXhwIjoxNzAyNTM5NTUyLCJjdG0iOjE2OTk5NDc1NTIxMTgsImNpZCI6ImQ5ZDBuNEFadXAifQ.XeViKuPpfkjZarNz-IUmhJ1jkOk5lSFc1v8dKB5hxL37JS7Xgb63EWDVghKjfPRAdW4iHCpikSCJFwa1-iC7RGBQfLjrQqO7NYIB-ZI8YlfcmxrhlDxNSMPgjcvZwYc6E_CxFopxHawN9zBfrLcAuZMFFQVQ2ooMZA2SIDBwgHBJJIktKmbwJueEcf7AdNvZw3x5vEe-KfLsBfcgnyffPpKvct4J8rVQNGXceQZ1SlS6cFZIg7e6CRErOyE7nl7yQPwrMqabQJdFhi-UNwekrNrjMqqH2opfQIMNcgYGvXAlQabOZ0u2P1bdg5xgDW06yAbR6UU_xH-qu49lKlDuxg; xq_r_token=e582d7d935fe508a65c8967a588fb3c2acb8a4d3; __utma=1.1859006477.1679307632.1697616458.1700647838.84; Hm_lvt_1db88642e346389874251b5a1eded6e3=1698644247,1700699665; acw_tc=2760779117007242621364913eb7b2720911cf4a0eca0f126e2221064fae47; is_overseas=0; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1700724265; snbim_minify=true',
    'Referer': 'https://xueqiu.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'elastic-apm-traceparent': '00-433c053faa6606229e132fc69ff4896b-e5f701e04597021b-00',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}

def get_bloggers_status(bloggers, commit_time, page=1):
    for blogger in bloggers:
        texts = []
        markdown_content = ""
        blogger_id = bloggers[blogger]
        for i in range(1, int(page)+1):
            url = bloggers_url.format(blogger_id, i)
            response = requests.get(url, headers=headers, cookies=cookies)
            data = response.json()
            try:
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
            except KeyError:
                print(blogger)


        # 定义Markdown文件名
        bloggers_file = "../../CSV/xueqiu/Bloggers/{0}{1}.md".format(blogger, commit_time)

        # 将结果转换为Markdown格式
        markdown_content = "### {}\n\n".format(blogger+commit_time)
        markdown_content += "\n*********************************************************************************\n".join(
            texts)

        # write to markdown
        with open(bloggers_file, "w", encoding="utf-8") as file:
            file.write(markdown_content)

get_bloggers_status(bloggers=bloggers, commit_time='2023-11-29', page=1)
