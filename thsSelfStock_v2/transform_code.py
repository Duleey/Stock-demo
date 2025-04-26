import base64
import os

from config_ths import ths_market_code

def decode_lnxn(code):
    # 使用 URL-safe Base64 解码, 但是/还是正常的
    data = base64.b64decode(code).decode('gbk')
    return data


def encode_lnxn(data):
    # 将字符串编码为 gbk 格式的字节数据
    gbk_bytes = data.encode('gbk')
    # 使用 Base64 编码
    data = base64.b64encode(gbk_bytes).decode('utf-8')

    return data


def matching_market_code(stock_code):
    # 读取code的数字部分
    code_num = ''.join(filter(str.isdigit, stock_code))
    if len(code_num) != 6:
        print("股票代码格式错误，请检查！")
        exit()
    for market in ths_market_code:
        for code_start in market['stock_code_start']:
            if code_num.startswith(code_start):
                print(f"匹配到{market['market_code']}市场股票代码：{code_num}")
                return market['market_code']

    print(f"股票{stock_code}未匹配到任何市场，请检查股票代码或设置！")
    exit()


if __name__ == '__main__':
    # 测试代码
    # 读取文件夹下所有文件名
    file_list = os.listdir(r'D:\StockData\stock-trading-data-pro')
    for file_name in file_list:
        matching_market_code(file_name)
