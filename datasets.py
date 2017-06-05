from flask import Flask,url_for,request,render_template
from tkinter import*
import time
from IBWrapper import IBWrapper,contract
from ib.ext.EClientSocket import EClientSocket
import pandas as pd
from datetime import datetime
import os
import numpy as np
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')
from datetime import datetime, timedelta
from pandas.lib import Timestamp
import pytz
#import datetime
import dateutil.relativedelta


import matplotlib.pyplot as plt
import timeit
import random


callback = IBWrapper()
tws = EClientSocket(callback)
host = ""
port = 7496
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

contract_Details1 = create.create_contract("ES","FUT","GLOBEX","USD",'','','20170616','50')#,expiry,mul)#,'','',exp4,multi) #"", "",
                                           #"20170317",
                                           #"50")  # ('NG', 'FUT', 'NYMEX', 'USD')
data_endtime = datetime.now().strftime("%Y%m%d %H:%M:%S")




Id = random.randint(0,1000000000)
tws.reqHistoricalData(Id, contract_Details1,data_endtime ,
                      '1 D',
                      '30 secs',
                      "TRADES",
                      1,
                      1)
#global data_ES
time.sleep(2)
data_ES = pd.DataFrame(callback.historical_Data,
                        columns=["reqId", "date", "open",
                                 "high", "low", "close",
                                 "volume", "count", "WAP",
                                 "hasGaps"])
#data_ES=data_ES.drop(data_ES.index[len(data_ES) - 1])

print (data_ES)



#data_endtime="20170510 12:00:00"
#d = datetime.today() - timedelta(days=2)
#date=d.strftime('%Y%m%d %H:%M:%S')
import datetime
times=30
for i in range(times):
        Id = random.randint(1, 1000)

        d = datetime.datetime.strptime(data_endtime, "%Y%m%d %H:%M:%S")
        d2 = d - dateutil.relativedelta.relativedelta(days=1)
        d2=d2.strftime('%Y%m%d %H:%M:%S')

        tws.reqHistoricalData(Id, contract_Details1,data_endtime ,
                              '1 D',
                              '30 secs',
                              "TRADES",
                              1,
                              1)
        #
        # global data_ES
        time.sleep(2)
        data_ES1 = pd.DataFrame(callback.historical_Data,
                                columns=["reqId", "date", "open",
                                         "high", "low", "close",
                                         "volume", "count", "WAP",
                                         "hasGaps"])
        #data_ES1 = data_ES1.drop(data_ES1.index[len(data_ES1) - 1])
        data_ES1=data_ES.append(data_ES1)


        d = datetime.datetime.strptime(d2, "%Y%m%d %H:%M:%S")
        d2 = d - dateutil.relativedelta.relativedelta(days=1)
        data_endtime=d2.strftime('%Y%m%d %H:%M:%S')

       # print (data_ES1)


time.sleep(3)
data_ES1.drop_duplicates('date',inplace=True)
data_ES1.replace('[]',np.nan)
ES=pd.DataFrame(data_ES1).sort_values(by='date')
ES.index=range(len(ES))
list=[-1,-1.00]
ES=ES.loc[~ES.volume.isin(list)]
d=random.randint(1,50)
#ma="E:/30 secs data" + "ID: %s" %d +".csv"

ES.to_csv("E:/2finalcheckES secs 30.csv")










tws.eDisconnect()
print("disconnected")



#open the csv file to which the new data is to be appended
with open('E:/demothis.csv', 'a') as f:
    (ES1).to_csv(f, header=False)

ES=pd.read_csv("")
