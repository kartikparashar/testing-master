
import time
from IBWrapper import IBWrapper,contract
from ib.ext.EClientSocket import EClientSocket
import pandas as pd
from datetime import datetime
import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from pandas.lib import Timestamp
import pytz
#import datetime
import dateutil.relativedelta
import random


callback = IBWrapper()
tws = EClientSocket(callback)
host = ""
port = 7497
clientId = 100

#connect
tws.eConnect(host, port, clientId)
print("connected")

time.sleep(2)
#read function from package into a variable
create = contract()
#callback function to fetch data into specified similar named columns
callback.initiate_variables()

#fetch from TWS 1st ticker

contract_Details1 = create.create_contract("NG","FUT","NYMEX","USD",'','','20170628','10000')

    #("ES","FUT","GLOBEX","USD",'','','20170616','50')#,expiry,mul)#,'','',exp4,multi) #"", "",
                                           #"20170317",



Id = random.randint(1, 1000)


tws.reqHistoricalData(Id, contract_Details1, "20170605 13:30:00",
                      '1 D',
                      '5 mins',
                      "TRADES",
                      0,
                      1)
time.sleep(2)
df = pd.DataFrame(callback.historical_Data,
                                columns=["reqId", "date", "open",
                                         "high", "low", "close",
                                         "volume", "count", "WAP",
                                         "hasGaps"])
#df=data_ES1
df=df.drop('hasGaps',axis=1)
df=df[["reqId","date","open","high","low","close","volume","WAP","count"]]
df=df.rename(index=str, columns={"date": "time", "WAP": "wap"})
df=df[:-1]

df.to_csv('E:/DATA.csv')