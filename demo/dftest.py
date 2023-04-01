"""
https://blog.csdn.net/csdndscs/article/details/125299254
"""

import pandas as pd

res = pd.DataFrame({'Bob': ['T like bob', 'it is awson'],
                    'sue': ['pretty good', 'Bland']},
                   index=['projectA', 'projectB'])
print(res)


res1 = pd.Series([1, 2, 3, 4, 5, 6])
print(res1)