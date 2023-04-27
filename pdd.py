import pandas as pd
from collections import OrderedDict

Dict = {
    '日期', ['2018-08-01', '2018-0802', '2018-0803'], '开盘价',
    ['001616528', '001616528', '0012602828']
}

salesOrderedDict = OrderedDict(Dict)
salesDf = pd.DataFrame(salesOrderedDict)
salesDf
