

import timeit
import random


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



###start of intializations
tf1 = 1
tf2 = 1
new_entry = 'T'
wdw = 25
sflag=0
j = 0
ctime = 0


#end of intializations


callback = IBWrapper()
tws = EClientSocket(callback)
host = ""
port = 7497
clientId = 100
create = contract()
callback.initiate_variables()



signalresult =pd.DataFrame({'price' : [],'avgprice' : [],'qty' : [],'signal' : [],'time' : [],'otype' : []})
signalinfo = pd.DataFrame({'price' : [],'qty' : [],'signal' : []})


#function to fetch execution details
def fetchexe():
    global signalresult
    tws.reqExecutions(order_id, create.exec_filter(clientId, ctrct[8], contract_info))
    exedetails = callback.exec_Details_execution.__dict__
    print(exedetails)
    # details to push into csv
    exeprice = exedetails['m_price']
    avgprice = exedetails['m_avgPrice']
    exeqty = exedetails['m_cumQty']
    exesignal = exedetails['m_side']
    exetime = exedetails['m_time']
    signalresult=signalresult.append({'price' : exeprice,'avgprice' : avgprice,'qty' : exeqty,'signal' : exesignal,'time' : exetime,'otype' : o_type},ignore_index=True)

    signalresult.to_csv('E:/signalresult1.csv')
    return
#function or quantity
def calqty(p_amt):
    cap_amt = 100000
    quant = max(int(round((cap_amt)/(p_amt * 10000))),1)
    return quant

##entry function
def entryfun(signal,price):
    global sflag,j#,o_type,qty):
    sflag = 0
    for j in range(3):
        # run for 5 mins ,30sec data

        tickerId = random.randint(1, 100000)
        tws.reqRealTimeBars(tickerId,
                            contract_Details1,
                            5,
                            "TRADES",
                            0)
        #time.sleep(1)
        data = pd.DataFrame(callback.real_timeBar,
                            columns=["reqId", "time", "open", "high", "low", "close", "volume", "wap",
                                     "count"]).tail(1)




        data=data.set_index(["time"])

        # data['time'] = pd.to_datetime(data['time'], unit='s')
        newprice = data.iloc[0]['close']


        if (signal == 'BUY') and (newprice < price):  # confirm
            price = newprice
            qty = calqty(newprice)
            o_type = "MKT"
            signal = 'BUY'
            order_id = callback.next_ValidId + 1
            callback.next_ValidId = order_id
            order_info = create.create_order(ctrct[8], o_type, qty, signal, price, True)

            #place order
            tws.placeOrder(order_id, contract_info, order_info)


            sflag = 1
            break
        elif (newprice > price) and (signal == 'SELL'):

            price = newprice
            qty = calqty(newprice)
            o_type = "MKT"
            signal = 'SELL'
            order_id = callback.next_ValidId + 1
            callback.next_ValidId = order_id
            order_info = create.create_order(ctrct[8], o_type, qty, signal, price, True)

            tws.placeOrder(order_id, contract_info, order_info)

            sflag = 1

            # write to csv
            break

        else:
            time.sleep(20)
    return










#start_time = timeit.default_timer()


#connect
tws.eConnect(host, port, clientId)
print("connected")

import time




#fetch from TWS 1st ticker
#get data from TWS

contract_Details1 = create.create_contract("NG","FUT","NYMEX","USD",'','','20170628','10000')#,expiry,mul)#,'','',exp4,multi) #"", "",
#,expiry,mul)#,'','',exp4,multi) #"", "",
                                           #"20170317",
                                           #"50")  # ('NG', 'FUT', 'NYMEX', 'USD')




df=pd.read_csv("E:/DATA.csv")
df=df.set_index(["time"])
#

# df = pd.DataFrame({'reqId' : [],'time' : [],'open' : [],'high' : [],
                  # 'low' : [],'close' : [],'volume' : [],'wap' : [],'count' : []})


#data_endtime = datetime.now().strftime("%Y%m%d %H:%M:%S")

#loop starts
tws.reqIds(1)
print("realtimedata")
times= 60

for i in range(times):

    tickerId = random.randint(1, 1000000)
    tws.reqRealTimeBars(tickerId,
                        contract_Details1,
                        5,
                        "TRADES",
                        0)
    time.sleep(1)
    data = pd.DataFrame(callback.real_timeBar,
                        columns=["reqId", "time", "open", "high", "low", "close", "volume", "wap", "count"]).tail(1)
    if data.empty:
         print("empty data")
         time.sleep(1)
         data = pd.DataFrame(callback.real_timeBar,
                             columns=["reqId", "time", "open", "high", "low", "close", "volume", "wap", "count"]).tail(1)



    data["time"] = data["time"].astype(str)
    #time.sleep(2)
    # duplicate removal
    data.drop_duplicates('time', inplace=True)
    data.replace('[]', np.nan)
    data['time'] = pd.to_datetime(data['time'], unit='s')
    data = data.set_index(["time"]).tz_localize("UTC").tz_convert("Asia/Kolkata")
    print(data)
    #data['time'] = pd.to_datetime(data['time'], unit='s')
    df=df.append(data)



    df.to_csv("E:/DATA.csv")
    ES=df[["close"]]
    #print(df1)

    #data_ES=data_ES.drop(data_ES.index[len(data_ES) - 1])
    #ES=pd.DataFrame(df1).sort_values(by='time')
    #ES.index=range(len(ES))
    #list=[-1,-1.00]
    #ES=ES.loc[~ES.volume.isin(list)]
    #d=random.randint(1,10)
    #ES=ES.set_index(["time"])
    #print (ES)

    #strategy mean
    mrf_df = ES.tail(25)
    mrf_df = mrf_df.assign(ma = pd.Series.rolling(mrf_df['close'], window=wdw).mean())
    mrf_df = mrf_df.assign(sd = pd.Series.rolling(mrf_df['close'], window=wdw).std())
    mrf_df['sd_up'] = mrf_df['ma'] + (0.5 * mrf_df['sd'])
    mrf_df['sd_dwn'] = mrf_df['ma'] - (0.5 * mrf_df['sd'])
    mrf_df = mrf_df.assign(signals = ['n'] * len(mrf_df))
    mrf_df = mrf_df.assign(sb_price = [0.0] * len(mrf_df))
    mrf_df = mrf_df.assign(stk_no = [0] * len(mrf_df))

    for k in mrf_df.index:
        #####when price crosses sd_u ##########
        if (new_entry == 'T'):
            if (mrf_df.loc[k, 'close'] > mrf_df.loc[k, 'sd_up']):
                mrf_df.loc[k, 'sb_price'] = mrf_df.loc[k, 'close']
                mrf_df.loc[k, 'signals'] = 'SELL'
                mrf_df.loc[k, 'stk_no'] = calqty(mrf_df.loc[k, 'close'])
                s_qty = mrf_df.loc[k, 'stk_no']
                tf1 = 0
                new_entry = 'F'

                ######crosses sd_l
            elif (mrf_df.loc[k, 'close'] < mrf_df.loc[k, 'sd_dwn']):
                mrf_df.loc[k, 'signals'] = 'BUY'
                mrf_df.loc[k, 'sb_price'] = mrf_df.loc[k, 'close']
                mrf_df.loc[k, 'stk_no'] = calqty(mrf_df.loc[k, 'close'])
                s_qty = mrf_df.loc[k, 'stk_no']
                tf2 = 0
                new_entry = 'F'

        elif(mrf_df.loc[k, 'sd_dwn'] < mrf_df.loc[k, 'close'] < mrf_df.loc[k, 'sd_up']):
            ####IF PRICE BETWEEN SDU AND SD1L#### EXIT OF TF1####
            if (tf1 == 0):
                mrf_df.loc[k, 'signals'] = 'BUY'
                mrf_df.loc[k, 'sb_price'] = mrf_df.loc[k, 'close']
                mrf_df.loc[k, 'stk_no'] = s_qty
                tf1 = 1
                new_entry = 'T'
                ####IF PRICE BETWEEN SDL AND SDU#### EXIT OF TF2####
            elif (tf2 == 0) :
                mrf_df.loc[k, 'signals'] = 'SELL'
                mrf_df.loc[k, 'sb_price'] = mrf_df.loc[k, 'close']
                mrf_df.loc[k, 'stk_no'] = s_qty
                tf2 = 1
                new_entry = 'T'


        elif (mrf_df.loc[k, 'close'] > mrf_df.loc[k, 'sd_up']) and (tf2 == 0):
            ###### price @tf2 = 0 reaches above sdu#######
            ####closing tf2 and becomes sell above sdu
            mrf_df.loc[k, 'sb_price'] = mrf_df.loc[k, 'close']
            nw_qty = calqty(mrf_df.loc[k, 'close'])
            mrf_df.loc[k, 'stk_no'] = s_qty + nw_qty
            ps_qty = s_qty
            s_qty = nw_qty
            tf2 = 1
            mrf_df.loc[k, 'signals'] = 'SELL'
            tf1 = 0
            new_entry = 'E'
            #####closing tf2###and becomenew buy @sdu
        elif (mrf_df.loc[k, 'close'] < mrf_df.loc[k, 'sd_dwn']) and (tf1 == 0):
            ####buy price@tf1 = 0 reaches below sd_l####close tf1###
            #########make that as a buy downside
            mrf_df.loc[k, 'sb_price'] = mrf_df.loc[k, 'close']
            nw_qty = calqty(mrf_df.loc[k, 'close'])
            mrf_df.loc[k, 'stk_no'] = s_qty + nw_qty
            ps_qty = s_qty
            s_qty = nw_qty
            tf1 = 1
            mrf_df.loc[k, 'signals'] = 'BUY'
            tf2 = 0
            new_entry = 'E'

    o_type = 'LMT'
    qty = mrf_df.iloc[-1, :].stk_no
    signal = mrf_df.iloc[-1, :].signals
    price = mrf_df.iloc[-1, :].sb_price

    qty = int(qty)
    price = float(price)
    signal = str(signal)
    o_type = str(o_type)
    signalinfo= signalinfo.append({'price': price ,'qty': qty, 'signal': signal},
        ignore_index=True)
    signalinfo.to_csv('E:/signalinfo.csv')

    if (signal == 'n'):
            time.sleep(299) #need to confirm sleep time and loop
    elif (signal != 'n'):
        #tws.reqIds(1)
        order_id = callback.next_ValidId + 1
        callback.next_ValidId = order_id

        #contract and order creation
        ctrct= ["NG", "FUT", "NYMEX", "USD", '', '', '20170628', '10000', "DU228380"]#
        contract_info = create.create_contract(ctrct[0], ctrct[1], ctrct[2],
                                               ctrct[3],ctrct[4],ctrct[5],ctrct[6],ctrct[7])
        order_info = create.create_order(ctrct[8],o_type,qty,signal,price,True)
        print(o_type,qty,signal,price)
        #time.sleep(2)

        #place order
        tws.placeOrder(order_id, contract_info, order_info)

        print("waiting for status")
        #sleep for 5 seconds(discuss)
        time.sleep(3)
        #getting order confirmation###

        confirm = pd.DataFrame(callback.order_Status,
                               columns=['orderId', 'status', 'filled', 'remaining', 'avgFillPrice',
                                   'permId', 'parentId', 'lastFillPrice', 'clientId', 'whyHeld'])

        check=confirm.tail(1)
        filled= check.iloc[0]['filled']
        remain=check.iloc[0]['remaining']
        #filled=confirm.iloc[-1, :].filled
        #remain = confirm.iloc[-1, :].remaining
        #details to push into csv

        ctime = 296

        if ((filled== qty) and (remain==0)):
            fetchexe()
            #write into csv
            time.sleep(ctime)

        elif((filled==0) and (remain== qty)):
             if ((tf1 == 1) and (new_entry == 'T')) or ((tf2 == 1) and (new_entry == 'T')) :#exit criteria
                 tws.cancelOrder(order_id)
                 order_id = callback.next_ValidId + 1
                 callback.next_ValidId = order_id
                 o_type="MKT"
                 order_info = create.create_order(ctrct[8], o_type, qty, signal, price, True)
                 tws.placeOrder(order_id, contract_info, order_info)
                 time.sleep(1)
                 fetchexe()

                 # to be written in csv ,do not re write the existing price variable

                 time.sleep(ctime-1)  #need to confirm

             elif((tf1 == 0) and (new_entry == 'F')) or ((tf2 == 0) and (new_entry == 'F')): ###entry
                 tws.cancelOrder(order_id)
                 entryfun(signal,price)
                 if sflag == 1:
                     s_qty = qty
                     time.sleep(1)
                     fetchexe()
                     ctime = ((ctime-1)-(j*20))
                     #write into csv
                 else:
                     tf1 = 1
                     tf2 = 1
                     new_entry = 'T'
                     print(j)
                     ctime = ctime - ((j-1)*20)



                 time.sleep(ctime)
             elif((tf1 == 0) and (new_entry == 'E')) or ((tf2 == 0) and (new_entry == 'E')): ###exit and entry
                 tws.cancelOrder(order_id)
                 order_id = callback.next_ValidId + 1
                 callback.next_ValidId = order_id
                 qty = ps_qty
                 o_type = "MKT"
                 order_info = create.create_order(ctrct[8], o_type, qty, signal, price, True)
                 tws.placeOrder(order_id, contract_info, order_info)
                 time.sleep(1)
                 fetchexe()
                 # write to csv


                 entryfun(signal,price)
                 if sflag == 1:
                     s_qty = qty####qty from the market order inside the function entryfun()
                     time.sleep(1)
                     fetchexe()
                     ctime = ((ctime - 2) - (j * 20))
                     # write into csv
                 else:
                     tf1 = 1
                     tf2 = 1
                     new_entry = 'T'
                     ctime = ((ctime-1)-((j-1)*20))
                 time.sleep(ctime)

    #partial fill
        elif (0 < filled < qty) and (remain >0) :

             fetchexe()
             #write into csv
             if ((tf1 == 1) and (new_entry == 'T')) or ((tf2 == 1) and (new_entry == 'T')) :#exit
                 qty = remain
                 o_type="MKT"
                 order_id = callback.next_ValidId + 1
                 callback.next_ValidId = order_id
                 order_info = create.create_order(ctrct[8], o_type, qty, signal, price, True)
                 tws.placeOrder(order_id, contract_info, order_info)
                 time.sleep(1)
                 fetchexe()

                 # to be written in csv ,do not re write the existing price variable
                 ctime = (ctime - 1)
                 time.sleep(ctime)  #need to confirm

             elif ((tf1 == 0) and (new_entry == 'F')) or ((tf2 == 0) and (new_entry == 'F')):  ###entry
                 entryfun(signal,price)
                 if sflag == 1 :
                     s_qty = filled + qty ###qty from the market order in the entryfun
                     time.sleep(1)
                     fetchexe()
                     ctime = ((ctime - 2) - (j * 20))
                     #write into csv
                 else:
                     s_qty = filled
                     ctime = ((ctime - 1) - ((j-1) * 20))
                 time.sleep (ctime)
             elif ((tf1 == 0) and (new_entry == 'E')) or ((tf2 == 0) and (new_entry == 'E')):  ###exit and entry
                  if (filled < ps_qty):
                      qty = (ps_qty - filled)
                      o_type = "MKT"
                      order_id = callback.next_ValidId + 1
                      callback.next_ValidId = order_id
                      order_info = create.create_order(ctrct[8], o_type, qty, signal, price, True)
                      tws.placeOrder(order_id, contract_info, order_info)
                      time.sleep(1)
                      fetchexe()
                      #write into csv
                      entryfun(signal,price)
                      if sflag == 1 :
                          s_qty = qty ###frm the market order inside the entry function
                          time.sleep(1)
                          fetchexe()
                          ctime = ((ctime - 2) - (j * 20))
                          # write into csv
                      else:
                          tf1 = 1
                          tf2 = 1
                          new_entry = 'T'
                          ctime = ((ctime - 1) - ((j-1) * 20))

                      time.sleep(ctime)

                  elif (filled > ps_qty) :
                      entryfun(signal,price)
                      if sflag == 1 :
                          s_qty = qty + (filled - ps_qty) ##qty is the qty from mkt orfer inside the entryfun
                          time.sleep(1)
                          fetchexe()
                          ctime = ((ctime - 1) - (j * 20))

                          #write into csv
                      else:
                          s_qty = (filled - ps_qty)
                          ctime = ctime - ((j-1) * 20)

                      time.sleep(ctime)
                  elif (filled == ps_qty):
                       entryfun(signal,price)
                       if sflag == 1:
                           s_qty = qty ##qty is the qty from mkt orfer inside the entryfun
                           time.sleep(1)
                           fetchexe()
                           ctime = ((ctime-1) - (j * 20))
                           #write into csv
                       else:
                           tf1 = 1
                           tf2 = 1
                           new_entry = 'T'
                           ctime = ctime - ((j-1) * 20)

                       time.sleep(ctime)








