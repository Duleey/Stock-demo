import os

from config_ths import add_signal
from operate import delete_custom_block
from config_ths import path_ths
from config_ths import user
from transform_code import decode_lnxn

if __name__ == '__main__':
    files_path = path_ths + r"/" + user + r"/custom_block"
    has_block = False
    # 循环file_path下的数字文件
    for file_name in os.listdir(files_path):
        if file_name.isdigit() and file_name != "0":
            # pandas读取文件
            # 读取为json
            with open(files_path + "/" + file_name, "r", encoding="utf-8") as f:
                data = f.read()
                # 解析json
                json_data = eval(data)
            if decode_lnxn(json_data["ln"]).endswith(add_signal):
                # 删除自定义板块
                delete_custom_block(decode_lnxn(json_data["ln"]))
