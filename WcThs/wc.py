import pywencai
import pandas as pd
from common.logger import Logger
import common.os_paths as path
import os
import datetime

# 获取当前时间
current_time = datetime.datetime.now().strftime("%Y-%m-%d")

name = "wc"

res = pywencai.getWencai(question='当日股票成交额大于20亿', secondary_intent='stock')

result = pd.DataFrame(res, columns=res.columns)
print(result)
result.to_excel(os.path.join(path.CSV_PATH, name + current_time + '.xls'), encoding="utf-8", index=False)
print("to_excel success to {}".format(os.path.join(path.CSV_PATH, name + + current_time + '.csv')))
