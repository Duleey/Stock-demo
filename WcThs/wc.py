import pywencai
import pandas as pd
from common.logger import Logger
import common.os_paths as path
import os

name = "wc"

res = pywencai.getWencai(question='共封装光学（CPO）,非ST,非科创板,非次新股,股价在5周均线上,收盘价>平均成本,近5个交易日涨幅<25%,5日线均线上移', secondary_intent='stock')

result = pd.DataFrame(res, columns=res.columns)
result.to_csv(os.path.join(path.CSV_PATH, name + '.xls'), encoding="utf-8", index=False)
print("to_excel success to {}".format(os.path.join(path.CSV_PATH, name + '.csv')))
