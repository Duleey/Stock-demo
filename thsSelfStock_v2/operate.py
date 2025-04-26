import os
import re

from transform_code import decode_lnxn, matching_market_code
from transform_code import encode_lnxn
from config_ths import path_ths
from config_ths import user
import pandas as pd
from datetime import datetime
import chardet  # 用于自动检测文件编码
import ast



def add_stock_to_custom_block(custom_block_name, stock_code_list):
    files_path = path_ths + r"/" + user + r"/custom_block"
    has_block = False
    # 循环file_path下的数字文件
    for file_name in os.listdir(files_path):
        # 数字文件为板块，其中0文件是汇总
        if file_name.isdigit() and file_name != "0":
            # 读取为json
            with open(files_path + "/" + file_name, "r", encoding="utf-8") as f:
                data = f.read()
                # 解析json
                json_data = eval(data)
            if decode_lnxn(json_data["ln"]) == custom_block_name:
                has_block = True
                # 解析 context 字段
                context = json_data["context"]
                # stock_code_list只保留数字部分
                stock_code_list = [''.join(filter(str.isdigit, code)) for code in stock_code_list]
                if len(context.split(",")) < 2:
                    new_stock_codes = stock_code_list
                    market_codes = [""]
                    stock_codes = [""]
                else:
                    # 解析context
                    stock_codes, market_codes = context.split(",")[0].split("|"), context.split(",")[1].split("|")
                    # 不在context中的股票代码
                    new_stock_codes = [code for code in stock_code_list if code not in stock_codes]
                for stock_code in new_stock_codes:
                    market_code = matching_market_code(stock_code)
                    # 加入到stock_codes的倒数第一个位置
                    stock_codes.insert(-1, stock_code)
                    market_codes.insert(-1, market_code)
                # 更新context
                context = "|".join(stock_codes) + "," + "|".join(market_codes)
                # print('更新板块成功, 文件名为：', file_name)
                # print('更新后的context为：', context)
                json_data["context"] = context
                # 写入新文件
                with open(files_path + "/" + file_name, "w", encoding="utf-8") as f:
                    f.write(str(json_data).replace("'", "\""))
                with open(files_path + r"/__base_/upload/" + file_name, "w", encoding="utf-8") as f:
                    f.write(str(json_data).replace("'", "\""))
                # 更新pc_common.ini文件
                version_increase(files_path, file_name)
                break
    if not has_block:
        raise Exception('板块不存在')


def new_custom_block(custom_block_name, use_empty=True):
    files_path = path_ths + r"/" + user + r"/custom_block"
    has_block = False
    # 循环file_path下的数字文件
    for file_name in os.listdir(files_path):
        # 数字文件为板块，其中0文件是汇总
        if file_name.isdigit() and file_name != "0":
            # 读取为json
            with open(files_path + "/" + file_name, "r", encoding="utf-8") as f:
                data = f.read()
                # 解析json
                json_data = eval(data)
            if decode_lnxn(json_data["ln"]) == custom_block_name:
                has_block = True
                print('板块已存在, 文件名为：', file_name)
    if not has_block:
        if use_empty:
            # 空白模块
            block_num = []
            # 寻找空白模块
            for file_name in os.listdir(files_path):
                if file_name.isdigit() and file_name != "0":
                    # 读取为json
                    with open(files_path + "/" + file_name, "r", encoding="utf-8") as f:
                        data = f.read()
                        # 解析json
                        json_data = eval(data)
                    if json_data["ln"] == "":
                        block_num.append(int(file_name))
            if len(block_num) > 0:
                # 找到数组最小的空白模块
                file_name = str(min(block_num))
                update_custom_block_ln(files_path, file_name, custom_block_name)
            else:
                print('没有空白模块, 直接创建')
                create_custom_block(custom_block_name, files_path)
        else:
            create_custom_block(custom_block_name, files_path)


def delete_custom_block(custom_block_name, del_file=False):
    files_path = path_ths + r"/" + user + r"/custom_block"
    has_block = False
    # 循环file_path下的数字文件
    for file_name in os.listdir(files_path):
        # 数字文件为板块，其中0文件是汇总
        if file_name.isdigit() and file_name != "0":
            # 读取为json
            with open(files_path + "/" + file_name, "r", encoding="utf-8") as f:
                data = f.read()
                # 解析json
                json_data = eval(data)
            if decode_lnxn(json_data["ln"]) == custom_block_name:
                has_block = True
                # 读取0文件
                with open(files_path + "/0", "r", encoding="utf-8") as f0:
                    data0 = f0.read()
                    # 解析json
                    json_data0 = eval(data0)
                # 在sortstr中删除'hex_num,'
                sortstr = json_data0["sortstr"]
                hex_num = hex(int(file_name))[2:].upper()
                sortstr = sortstr.replace(hex_num + ",", "")
                # 更新0文件
                json_data0["sortstr"] = sortstr
                # 写入0文件
                with open(files_path + "/0", "w", encoding="utf-8") as f0:
                    f0.write(str(json_data0).replace("'", "\""))
                # 删除文件
                if del_file:
                    os.remove(files_path + "/" + file_name)
                else:
                    json_data["ln"] = ""
                    json_data["xn"] = ""
                    json_data["context"] = ""
                    # 写入新文件
                    with open(files_path + "/" + file_name, "w", encoding="utf-8") as f:
                        f.write(str(json_data).replace("'", "\""))
                    with open(files_path + r"/__base_/upload/" + file_name, "w", encoding="utf-8") as f:
                        f.write(str(json_data).replace("'", "\""))
                # 更新pc_common.ini文件
                version_increase(files_path, file_name)
                print('删除板块成功, 文件名为：', file_name)
                break
    if not has_block:
        raise Exception


def create_custom_block(custom_block_name, files_path):
    new_file_name = 1  # 跳过0文件
    has_find = False  # 是否找到已经创建的文件
    while True:
        if new_file_name >= 200:
            print('创建失败, 超过最大文件数, 如果没有模块，请先创建一个')
            break
        if not os.path.exists(files_path + "/" + str(new_file_name)) and not has_find:
            new_file_name += 1
            continue
        if os.path.exists(files_path + "/" + str(new_file_name)) and not has_find:
            has_find = True
            new_file_name += 1
            continue
        if os.path.exists(files_path + "/" + str(new_file_name)) and has_find:
            new_file_name += 1
            continue
        if not os.path.exists(files_path + "/" + str(new_file_name)) and has_find:
            # 创建新文件
            new_json_data = {"context": "", "ln": encode_lnxn(custom_block_name), "xn": ""}
            # 将文件名转换为数字
            file_num = int(new_file_name)
            # 转换为16进制
            hex_num = hex(file_num)[2:].upper()
            # 读取0文件
            with open(files_path + "/0", "r", encoding="utf-8") as f0:
                data0 = f0.read()
                # 解析json
                json_data0 = eval(data0)
                # 在sortstr中加入'hex_num,'
                json_data0["sortstr"] = json_data0["sortstr"] + hex_num + ","
            # 写入0文件
            with open(files_path + "/0", "w", encoding="utf-8") as f0:
                f0.write(str(json_data0).replace("'", "\""))
            # 保存文件
            with open(files_path + "/" + str(new_file_name), "w", encoding="utf-8") as f:
                f.write(str(new_json_data).replace("'", "\""))
            # 更新pc_common.ini文件
            version_increase(files_path, new_file_name)
            print('创建板块成功, 文件名为：', new_file_name)
            break


def update_custom_block_ln(files_path, file_name, ln):
    with open(files_path + "/" + file_name, "r", encoding="utf-8") as f:
        data = f.read()
        # 解析json
        json_data = eval(data)
    json_data["ln"] = encode_lnxn(ln)
    # 将文件名转换为数字
    file_num = int(file_name)
    # 转换为16进制
    hex_num = hex(file_num)[2:].upper()
    # 读取0文件
    with open(files_path + "/0", "r", encoding="utf-8") as f0:
        data0 = f0.read()
        # 解析json
        json_data0 = eval(data0)
        # 在sortstr中加入'hex_num,'
        json_data0["sortstr"] = json_data0["sortstr"] + hex_num + ","
    # 写入0文件
    with open(files_path + "/0", "w", encoding="utf-8") as f0:
        f0.write(str(json_data0).replace("'", "\""))
    # 写入新文件
    with open(files_path + "/" + file_name, "w", encoding="utf-8") as f:
        f.write(str(json_data).replace("'", "\""))
    with open(files_path + r"/__base_/upload/" + file_name, "w", encoding="utf-8") as f:
        f.write(str(json_data).replace("'", "\""))
    print('修改板块成功, 文件名为：', file_name)
    # 更新pc_common.ini文件
    version_increase(files_path, file_name)


def version_increase(files_path, file_name):
    # 将文件名转换为数字
    file_num = int(file_name)
    # 转换为16进制
    hex_num = hex(file_num)[2:].upper()
    # 补全到6位
    hex_num = hex_num.zfill(6)
    # 读取pc_common.ini文件
    with open(files_path + "/pc_common.ini", "r", encoding="utf-8") as f:
        data = f.read()
        # 截取[index_code_version]及之前的内容
        data1 = data[:data.find("[index_code_version]") + 20]
        # 截取[index_code_version]之后的内容
        data2 = data[data.find("[index_code_version]") + 20:]
        # 匹配'hex_num=%d'
        pattern = hex_num + r"=(\d+)"
        if re.search(pattern, data2) is None:
            # 直接在data2末尾添加'hex_num=0'
            data2_new = data2 + hex_num + "=0"
        else:
            # 匹配'hex_num=%d'并替换为'hex_num=%d+1'
            match = re.search(pattern, data2).group(1)
            # 版本号加1
            new_version = int(match) + 1
            # 写入pc_common.ini文件
            data2_new = data2.replace(re.search(pattern, data2).group(), re.search(pattern, data2).group(0)[:-len(re.search(pattern, data2).group(1))] + str(new_version))

        # 匹配'hex_num='到下一个'='
        pattern = rf'^{hex_num}=.*'
        stock_str = ''
        # 读取文件,如果文件存在，则读取context字段重新拼接stock_str，否则stock_str为空则在pc_common.ini中删除这一行
        if os.path.exists(files_path + "/" + str(file_name)):
            with open(files_path + "/" + file_name, "r", encoding="utf-8") as f:
                data = f.read()
                # 解析json
                json_data = eval(data)
                context = json_data["context"]
                if context != '':
                    stock_codes, market_codes = context.split(",")[0].split("|"), context.split(",")[1].split("|")
                    for i in range(len(stock_codes)):
                        if stock_codes[i] == '':
                            continue
                        stock_str += market_codes[i] + ':' + stock_codes[i] + ','
        if re.search(pattern, data1, re.MULTILINE) is not None:
            match = re.search(pattern, data1, re.MULTILINE).group(0)
            if stock_str == '':
                # 删除这一行
                # 将数据按行分割
                lines = data1.splitlines()
                # 过滤掉匹配的行
                new_lines = []
                for line in lines:
                    if not re.match(pattern, line):
                        new_lines.append(line)
                # 重新拼接为字符串
                data1_new = '\n'.join(new_lines)
            else:
                # 替换这一行
                data1_new = data1.replace(match, match + stock_str)
        else:
            # 直接在data1倒数第二行添加’hex_num=‘ + stock_str
            if stock_str == '':
                data1_new = data1
            else:
                # 将数据按行分割
                lines = data1.splitlines()
                # 将'hex_num=stock_str'插入到倒数第二行
                new_lines = lines[:-1] + [hex_num + "=" + stock_str] + [lines[-1]]
                # 重新拼接为字符串
                data1_new = '\n'.join(new_lines)
        data_new = data1_new + data2_new
        # print(data_new)
        # exit()
        # 写入新文件
        with open(files_path + "/pc_common.ini", "w", encoding="utf-8") as f:
            f.write(data_new)
        # print(data_new)


def detect_file_encoding(file_path):
    """自动检测文件编码"""
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read(10000))
    return result['encoding']


def parse_special_csv(file_path, encoding):
    """解析特殊格式的CSV文件"""
    with open(file_path, 'r', encoding=encoding) as f:
        # 读取第一行获取列名
        columns_line = f.readline().strip()
        # 去除方括号和引号，然后分割列名
        columns = [col.strip() for col in columns_line[1:-1].replace("'", "").split(',')]

        # 读取剩余行作为数据
        data_lines = [line.strip() for line in f.readlines() if line.strip()]

    # 解析数据行
    data = []
    for line in data_lines:
        # 提取方括号内的数据部分
        data_part = line[line.find('[') + 1:line.find(']')]
        # 安全评估字符串为Python字面量
        try:
            row_data = ast.literal_eval(f"[{data_part}]")
            data.append(row_data)
        except:
            continue

    # 创建DataFrame
    df = pd.DataFrame(data, columns=columns)
    return df


def calculate_limit_up_streak(file_path):
    """计算单个股票的涨停连板数"""
    try:
        # 检测文件编码
        encoding = detect_file_encoding(file_path) or 'gbk'

        # 解析特殊格式的CSV
        df = parse_special_csv(file_path, encoding)

        if df.empty:
            print(f"文件 {file_path} 无有效数据")
            return None

        # 确保必要的列存在且为正确类型
        required_cols = ['股票代码', '股票名称', '交易日期', '收盘价', '前收盘价']
        for col in required_cols:
            if col not in df.columns:
                print(f"文件 {file_path} 缺少必要列: {col}")
                return None

        # 转换数据类型
        df['收盘价'] = pd.to_numeric(df['收盘价'], errors='coerce')
        df['前收盘价'] = pd.to_numeric(df['前收盘价'], errors='coerce')
        df = df.dropna(subset=['收盘价', '前收盘价'])

        # 按交易日期排序
        df['交易日期'] = pd.to_datetime(df['交易日期'])
        df = df.sort_values('交易日期')

        # 计算涨停价 (考虑不同板块的涨停幅度)
        def calculate_limit_price(row):
            code = str(row['股票代码'])
            name = str(row['股票名称'])

            # 北交所股票30%
            if code.startswith('bj'):
                return round(row['前收盘价'] * 1.3, 2)
            # ST股票5%
            elif 'ST' in name or '*ST' in name:
                return round(row['前收盘价'] * 1.05, 2)
            # 创业板、科创板20%
            elif code.startswith(('sh688', 'sz300')):
                return round(row['前收盘价'] * 1.2, 2)
            # 其他股票10%
            else:
                return round(row['前收盘价'] * 1.1, 2)

        df['涨停价'] = df.apply(calculate_limit_price, axis=1)

        # 判断是否涨停 (考虑浮点数精度)
        df['涨停'] = (abs(df['收盘价'] - df['涨停价']) < 0.01).astype(int)

        # 计算连板次数
        df['连板次数'] = df['涨停'].groupby((df['涨停'] != df['涨停'].shift()).cumsum()).cumsum()

        # 获取最新数据
        latest = df.iloc[-1]

        # 计算近1年数据
        one_year_ago = latest['交易日期'] - pd.Timedelta(days=365)
        one_year_df = df[df['交易日期'] >= one_year_ago]

        # 计算最大连板数
        def max_streak(s):
            return s.groupby(s.ne(s.shift()).cumsum()).max() if not s.empty else 0

        return {
            'ts_code': os.path.splitext(os.path.basename(file_path))[0],
            'name': latest['股票名称'],
            '最新连板': latest['连板次数'],
            '近1年涨停次数': one_year_df['涨停'].sum(),
            '近1年最大连板': max_streak(one_year_df['连板次数']),
            'trade_date': latest['交易日期'].strftime('%Y-%m-%d'),
            '收盘价': latest['收盘价'],
            '涨停价': latest['涨停价'],
            '板块': '北交所' if latest['股票代码'].startswith('bj') else
            '科创板' if latest['股票代码'].startswith('sh688') else
            '创业板' if latest['股票代码'].startswith('sz300') else '主板'
        }
    except Exception as e:
        print(f"处理文件 {file_path} 出错: {str(e)}")
        return None


def process_all_stocks(data_folder):
    """处理所有股票CSV文件"""
    results = []
    processed_files = 0

    for filename in os.listdir(data_folder):
        if filename.endswith('.csv'):
            file_path = os.path.join(data_folder, filename)
            result = calculate_limit_up_streak(file_path)
            if result:
                if result['最新连板'] > 0:
                    results.append(result)
                processed_files += 1

            if processed_files % 100 == 0:
                print(f"已处理 {processed_files} 个文件... 当前找到 {len(results)} 只连板股票")

    return pd.DataFrame(results)

if __name__ == '__main__':
    # 测试
    #version_increase(r"D:\同花顺软件\同花顺\mo_546889836\custom_block", 36)
    print(process_all_stocks(data_folder = 'D:\workspace\quant_data\stock-trading-data-pro'))
