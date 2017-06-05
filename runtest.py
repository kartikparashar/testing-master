import time
from IBWrapper import IBWrapper,contract
from ib.ext.EClientSocket import EClientSocket
import pandas as pd
import timeit
import random




callback = IBWrapper()
tws = EClientSocket(callback)
host = ""
port = 7496
clientId = 100
start_time = timeit.default_timer()
#connect
tws.eConnect(host, port, clientId)
print("connected")
time.sleep(2)
create = contract()
callback.initiate_variables()

#fetch from TWS 1st ticker

start_time = timeit.default_timer()
contract_Details1 = create.create_contract("ES","FUT","GLOBEX","USD",'','','20170616','50')



tickerId = random.randint(0,1000)
print(tickerId)
tws.reqRealTimeBars(tickerId,
                    contract_Details1,
                    5,
                    "TRADES",
                    0)
time.sleep(2)
df=pd.DataFrame(callback.real_timeBar,
             columns = ["reqId", "time", "open", "high", "low", "close", "volume", "wap", "count"])
#df=df.tail(1)
df['time'] = pd.to_datetime(df['time'],unit='s')
df1=df.set_index(["time"]).tz_localize("UTC").tz_convert("EST")
#df1=df1.tz_localize("UTC")
#df2=df1.tz_convert("EST")
#df1=df1[['close']]




time.sleep(60)
times=3
for i in range(times):
        tickerId = random.randint(1, 10000)
        tws.reqRealTimeBars(tickerId,
                            contract_Details1,
                            5,
                            "TRADES",
                            0)
        data=pd.DataFrame(callback.real_timeBar,
             columns = ["reqId", "time", "open", "high", "low", "close", "volume", "wap", "count"]).tail(1)
        data['time'] = pd.to_datetime(data['time'], unit='s')

        data = data.set_index(["time"]).tz_localize("UTC").tz_convert("EST")
        #data1 = data1.tz_localize("UTC")
        #data2 = data1.tz_convert("Asia/Kolkata")
        #data = data[['close']]



        df1=df1.append(data)
        #print(df2)
        time.sleep(60)



print("result")
print("**************************")
print(df1)
print("**************************")
df1.to_csv("E:/realtime.csv")
elapsed = timeit.default_timer() - start_time
print(elapsed)
tws.eDisconnect











