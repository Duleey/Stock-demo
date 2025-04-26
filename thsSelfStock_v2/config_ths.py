path_ths = r'D:\同花顺软件\同花顺'  # 同花顺安装路径,可以右键快捷方式，点击打开文件所在的位置找到
user = 'mo_5468'  # 同花顺用户名，在右上角查看
add_signal = '_py'   # 程序添加的自定义板块名称后缀标记，方便一键删除

#  同花顺市场代码（可自行补充）
ths_market_code = [
    {
        'market_code': '17',
        'stock_code_start': ['600', '601', '603', '605'],
        'distribution': '沪市主板 A 股'
    },
    {
        'market_code': '33',
        'stock_code_start': ['000', '001', '002', '003'],
        'distribution': '深市主板 A 股'
    },
    {
        'market_code': '32',
        'stock_code_start': ['300', '301', '302'],
        'distribution': '创业板'
    },
    {
        'market_code': '17',
        'stock_code_start': ['688', '689'],
        'distribution': '科创板'
    },
    {
        'market_code': '151',
        'stock_code_start': ['83', '87', '88', '43', '920'],
        'distribution': '北交所'
    },
]