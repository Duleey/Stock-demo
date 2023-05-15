#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/15 10:39 下午
# @Author  : jianwei.lv

from crawler.xueqiu import get_bloggers_status, get_portfolios

# 定义Markdown文件名
markdown_file = "../CSV/results.md"

def write_to_markdown(file_name, content):
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(content)

    # 将结果转换为Markdown格式
    markdown_content = "### Bloggers\n\n"
    markdown_content += "\n\n".join(res)

    markdown_content += "\n\n### Portfolios\n\n"
    markdown_content += res1

# 调用函数进行监控
res = get_bloggers_status(bloggers)
res1 = get_portfolios(portfolios)

# 将结果转换为Markdown格式
markdown_content = "### Bloggers\n\n"
markdown_content += "\n\n".join(res)

markdown_content += "\n\n### Portfolios\n\n"
markdown_content += res1

# 写入Markdown文件
write_to_markdown(markdown_file, markdown_content)
