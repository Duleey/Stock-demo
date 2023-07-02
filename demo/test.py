#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/15 11:09 下午
# @Author  : jianwei.lv

import requests

headers = {
    'Host': '111.173.104.159:8889',
    'Upgrade-Insecure-Requests': '1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1',
    'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
}

response = requests.get('http://111.173.104.159:8889/down.php/2b2797e120f1b342fc991a975daa33ce.pdf', headers=headers)
print(response.text)