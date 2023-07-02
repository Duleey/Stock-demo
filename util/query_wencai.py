import pywencai
import pandas as pd
from common.logger import Logger
import common.os_paths as path
import os
from common.wc_manager import WcManager

class QueryWc():
    def __init__(self):
        pass

    def wc_xls(self, question, name, colums, rename,secondary_intent='zhishu'):
        # 获取数据
        res = pywencai.getWencai(question=question, secondary_intent=secondary_intent)
        # 截取需要的列
        solve_result = res[colums]
        # 修改列名
        sovled_result = solve_result.rename(columns=rename)
        sovled_result.to_excel(os.path.join(path.CSV_PATH, name + '.xls'), encoding="utf-8", index=False)
        print("to_excel success to {}".format(os.path.join(path.CSV_PATH, name + '.xls')))

if __name__ == '__main__':
    from common.wc_manager import WcManager
    wcm = WcManager(start_time="2023.06.18")
    qwc = QueryWc()
    question, colums, rename = wcm.liangly()
    qwc.wc_xls(question=question, name="lly", colums=colums, rename=rename)