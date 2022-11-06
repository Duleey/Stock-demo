import pywencai
import pandas as pd
from common.logger import Logger
import common.os_paths as path
import os


name = "wc"

# 获取数据
res = pywencai.getWencai(question='两连阴概念板块;2022.11.03涨幅；2日涨幅；2022.11.03换手率; 2022.11.04涨幅; 2022.11.04换手率',
                         secondary_intent='zhishu')
result = pd.DataFrame(res)
# 截取需要的列
solve_result = res[['code', '指数简称', '指数@换手率[20221103]', '指数@换手率[20221104]',
                    '指数@涨跌幅:前复权[20221103]', '指数@涨跌幅:前复权[20221104]', '指数@区间涨跌幅:不复权[20221103-20221104]']]
# 修改列名
sovled_result = solve_result.rename(columns={"code": "代码",
                                             "指数@换手率[20221103]": "前一天换手率",
                                             "指数@换手率[20221104]": "今日换手率",
                                             "指数@涨跌幅:前复权[20221103]": "前一天涨幅%",
                                             "指数@涨跌幅:前复权[20221104]": "今日涨幅%",
                                             "指数@区间涨跌幅:不复权[20221103-20221104]": "两日涨幅%"})

sovled_result.to_excel(os.path.join(path.CSV_PATH, name + '.xls'), encoding="utf-8", index=False)
print("to_excel success to {}".format(os.path.join(path.CSV_PATH, name + '.xls')))
