import pywencai
import pandas as pd
from common.logger import Logger
import common.os_paths as path
import os


name = "wc"

res = pywencai.getWencai(question='两连阴行业板块；1天前涨幅；2日涨幅', secondary_intent='zhishu', start_time=2022-10-10)


result = pd.DataFrame(res, columns=res.columns)
result.to_csv(os.path.join(path.CSV_PATH, name + '.xls'), encoding="utf-8", index=False)
print("to_excel success to {}".format(os.path.join(path.CSV_PATH, name + '.csv')))
