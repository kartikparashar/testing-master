
import timeit
import random


import time
from IBWrapper import IBWrapper ,contract
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
from datetime import datetime
from pandas.lib import Timestamp
import pytz
# import datetime
import dateutil.relativedelta



###start of intializations
tf1 = 1
tf2 = 1
new_entry = 'T'
wdw = 25
ctime = 0
r_sflag = 0
r_qty = 0
cnt = 0
global o_type ,order_id

# end of intializations


callback = IBWrapper()
tws = EClientSocket(callback)
host = ""
port = 7497
clientId = 100
create = contract()
callback.initiate_variables()
tws.eConnect(host, port, clientId)
print("connected")
####dummy data request
contract_Details1 = create.create_contract("ES" ,"FUT" ,"GLOBEX" ,"USD" ,'' ,'' ,'20170616' ,'50')
tickerId = random.randint(1, 1000000)
# print(datetime.now())
tws.reqRealTimeBars(tickerId,
                    contract_Details1,
                    5,
                    "TRADES",
                    0)
ddata = list(callback.real_timeBar)
ddata = pd.DataFrame(callback.real_timeBar,
                     columns=["reqId", "time", "open", "high", "low", "close", "volume", "wap",
                              "count"])
print("dummy data: ")
print(ddata)

signalresult =pd.DataFrame({'price': [], 'avgprice': [], 'qty': [], 'signal': [], 'time': [], 'otype': []})
signalinfo = pd.DataFrame({'price': [], 'qty': [], 'signal': []})


# function to fetch execution details
def fetchexe(order_id):
    global signalresult
    tws.reqExecutions(order_id, create.exec_filter(clientId, ctrct[8], contract_info))
    exedetails = callback.exec_Details_execution.__dict__
    # print(exedetails)
    # details to push into csv
    exeprice = exedetails['m_price']
    avgprice = exedetails['m_avgPrice']
    exeqty = exedetails['m_cumQty']
    exesignal = exedetails['m_side']
    exetime = exedetails['m_time']

    signalresult = signalresult.append(
        {'price': exeprice, 'avgprice': avgprice, 'qty': exeqty, 'signal': exesignal, 'time': exetime, 'otype': o_type},
        ignore_index=True)

    signalresult.to_csv('E:/signalresult1.csv')
    return


# function or quantity
def calqty(p_amt):
    cap_amt = 100000
    quant = max(int(round((cap_amt) / (p_amt * 10000))), 1)
    return quant


##entry function
def entryfun(fsignal, fprice):
    # global sflag,j
    sflag = 0
    fqty = 0
    j = 0

    for j in range(10):
        # run for 30secs 5 mins data

        tickerId = random.randint(1, 100000)
        tws.reqRealTimeBars(tickerId,
                            contract_Details1,
                            5,
                            "TRADES",
                            0)
        time.sleep(1)
        data = pd.DataFrame(callback.real_timeBar,
                            columns=["reqId", "time", "open", "high", "low", "close", "volume", "wap",
                                     "count"]).tail(1)

        data = data.set_index(["time"])

        # data['time'] = pd.to_datetime(data['time'], unit='s')
        newprice = data.iloc[0]['close']
        print("new price:")
        print(newprice)

        if (fsignal == 'BUY') and (newprice < fprice):  # confirm
            fprice = newprice
            fqty = calqty(newprice)
            o_type = "MKT"
            fsignal = 'BUY'
            order_id = callback.next_ValidId + 1
            callback.next_ValidId = order_id
            order_info = create.create_order(ctrct[8], o_type, fqty, fsignal, fprice, True)

            # place order
            tws.placeOrder(order_id, contract_info, order_info)

            sflag = 1
            break
        elif (newprice > fprice) and (fsignal == 'SELL'):

            fprice = newprice
            fqty = calqty(newprice)
            o_type = "MKT"
            fsignal = 'SELL'
            order_id = callback.next_ValidId + 1
            callback.next_ValidId = order_id
            order_info = create.create_order(ctrct[8], o_type, fqty, fsignal, fprice, True)

            tws.placeOrder(order_id, contract_info, order_info)

            sflag = 1

            # write to csv
            break

        else:
            # print(j)
            time.sleep(29)

    return sflag, j, fqty











    # start_time = timeit.default_timer()


# connect





# fetch from TWS 1st ticker
# get data from TWS

# contract_Details1 = create.create_contract("ES","FUT","GLOBEX","USD",'','','20170616','50')#,expiry,mul)#,'','',exp4,multi) #"", "",
# ,expiry,mul)#,'','',exp4,multi) #"", "",
# "20170317",
# "50")  # ('NG', 'FUT', 'NYMEX', 'USD')




df = pd.read_csv("E:/DATA.csv")
df = df.set_index(["time"])
#

# df = pd.DataFrame({'reqId' : [],'time' : [],'open' : [],'high' : [],
# 'low' : [],'close' : [],'volume' : [],'wap' : [],'count' : []})


# data_endtime = datetime.now().strftime("%Y%m%d %H:%M:%S")

# loop starts
tws.reqIds(1)
times = 36
from datetime import datetime

for i in range(times):
    start_time1 = timeit.default_timer()
    tickerId = random.randint(1, 1000000)
    # print(datetime.now())
    tws.reqRealTimeBars(tickerId,
                        contract_Details1,
                        5,
                        "TRADES",
                        0)
    if i == 0:
        # time.sleep(4)
        data = list(callback.real_timeBar)

        data = pd.DataFrame(data,
                            columns=["reqId", "time", "open", "high", "low", "close", "volume", "wap", "count"]).tail(1)
        # data = pd.DataFrame(data.iloc[-1, :]).transpose()
        # print(data)
    else:
        data = list(callback.real_timeBar)

        data = pd.DataFrame(data,
                            columns=["reqId", "time", "open", "high", "low", "close", "volume", "wap", "count"]).tail(1)
        # data = pd.DataFrame(data.iloc[-1, :]).transpose()
        # print(data)
        # if data.empty:

        # print("empty data")
        # time.sleep(1)
        # time.sleep(2)
        # data = pd.DataFrame(callback.real_timeBar,
        # columns=["reqId", "time", "open", "high", "low", "close", "volume", "wap", "count"])

    data["time"] = data["time"].astype(str)
    # time.sleep(2)
    # duplicate removal
    # data.drop_duplicates('time', inplace=True)
    # data.replace('[]', np.nan)
    data['time'] = pd.to_datetime(data['time'], unit='s')
    data = data.set_index(["time"]).tz_localize("UTC").tz_convert("Asia/Kolkata")
    print(data)
    print(datetime.now())

    # data['time'] = pd.to_datetime(data['time'], unit='s')
    df = df.append(data)
    df.drop_duplicates('time', inplace=True)
    df.replace('[]', np.nan)

    df.to_csv("E:/DATA.csv")
    ES = df[["close"]]
    # print(df1)

    # data_ES=data_ES.drop(data_ES.index[len(data_ES) - 1])
    # ES=pd.DataFrame(df1).sort_values(by='time')
    # ES.index=range(len(ES))
    # list=[-1,-1.00]
    # ES=ES.loc[~ES.volume.isin(list)]
    # d=random.randint(1,10)
    # ES=ES.set_index(["time"])
    # print (ES)

    # strategy mean
    mrf_df = ES.tail(25)
    mrf_df = mrf_df.assign(ma=pd.Series.rolling(mrf_df['close'], window=wdw).mean())
    mrf_df = mrf_df.assign(sd=pd.Series.rolling(mrf_df['close'], window=wdw).std())
    mrf_df['sd_up'] = mrf_df['ma'] + (0.5 * mrf_df['sd'])
    mrf_df['sd_dwn'] = mrf_df['ma'] - (0.5 * mrf_df['sd'])
    mrf_df = mrf_df.assign(signals=['n'] * len(mrf_df))
    mrf_df = mrf_df.assign(sb_price=[0.0] * len(mrf_df))
    mrf_df = mrf_df.assign(stk_no=[0] * len(mrf_df))

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

        elif (mrf_df.loc[k, 'sd_dwn'] < mrf_df.loc[k, 'close'] < mrf_df.loc[k, 'sd_up']):
            ####IF PRICE BETWEEN SDU AND SD1L#### EXIT OF TF1####
            if (tf1 == 0):
                mrf_df.loc[k, 'signals'] = 'BUY'
                mrf_df.loc[k, 'sb_price'] = mrf_df.loc[k, 'close']
                mrf_df.loc[k, 'stk_no'] = s_qty
                tf1 = 1
                new_entry = 'T'
                ####IF PRICE BETWEEN SDL AND SDU#### EXIT OF TF2####
            elif (tf2 == 0):
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
    signalinfo = signalinfo.append({'price': price, 'qty': qty, 'signal': signal},
                                   ignore_index=True)
    signalinfo.to_csv('E:/signalinfo.csv')
    end1 = timeit.default_timer() - start_time1

    if (signal == 'n'):
        stime = 3600 - end1
        print(end1, stime)
        time.sleep(stime)
    elif (signal != 'n'):
        start_time2 = timeit.default_timer()
        # tws.reqIds(1)
        order_id = callback.next_ValidId + 1
        callback.next_ValidId = order_id

        # contract and order creation
        ctrct = ["ES", "FUT", "GLOBEX", "USD", '', '', '20170616', '50', "DU228380"]  #
        contract_info = create.create_contract(ctrct[0], ctrct[1], ctrct[2],
                                               ctrct[3], ctrct[4], ctrct[5], ctrct[6], ctrct[7])
        order_info = create.create_order(ctrct[8], o_type, qty, signal, price, True)
        print(o_type, qty, signal, price)
        # time.sleep(2)

        # place order
        tws.placeOrder(order_id, contract_info, order_info)

        # sleep for 5 seconds(discuss)
        time.sleep(3)
        # getting order confirmation###

        confirm = pd.DataFrame(callback.order_Status,
                               columns=['orderId', 'status', 'filled', 'remaining', 'avgFillPrice',
                                        'permId', 'parentId', 'lastFillPrice', 'clientId', 'whyHeld'])

        check = confirm.tail(1)
        filled = check.iloc[0]['filled']
        remain = check.iloc[0]['remaining']
        # filled=confirm.iloc[-1, :].filled
        # remain = confirm.iloc[-1, :].remaining
        # details to push into csv
        end2 = timeit.default_timer() - start_time2
        ctime = 3600 - (end1 + end2)

        if ((filled == qty) and (remain == 0)):
            print(end2, ctime)
            time.sleep(ctime)
            fetchexe(order_id)  ###fetching execution details and writing in csv

        elif ((filled == 0) and (remain == qty)):
            if ((tf1 == 1) and (new_entry == 'T')) or ((tf2 == 1) and (new_entry == 'T')):  # exit criteria
                start_time3 = timeit.default_timer()
                tws.cancelOrder(order_id)
                order_id = callback.next_ValidId + 1
                callback.next_ValidId = order_id
                o_type = "MKT"
                order_info = create.create_order(ctrct[8], o_type, qty, signal, price, True)
                tws.placeOrder(order_id, contract_info, order_info)
                end3 = timeit.default_timer() - start_time3
                ctime = ctime - end3
                print(end3, ctime)
                # to be written in csv ,do not re write the existing price variable
                time.sleep(ctime)  # need to confirm
                fetchexe(order_id)
            elif ((tf1 == 0) and (new_entry == 'F')) or ((tf2 == 0) and (new_entry == 'F')):  ###entry
                start_time4 = timeit.default_timer()
                tws.cancelOrder(order_id)
                # start_time = timeit.default_timer()
                r_sflag, cnt, r_qty = entryfun(signal, price)
                # endl = timeit.default_timer()- start_time
                end4 = timeit.default_timer() - start_time4

                if r_sflag == 1:
                    s_qty = r_qty
                    # time.sleep(1)
                    # fetchexe(order_id)
                    # ctime = ((ctime-1)- (cnt*20))#####4 is for entryfun 1 for fetchexe
                    ctime = ctime - end4
                    print(end4, ctime)
                    time.sleep(ctime)
                    # write into csv
                    fetchexe(order_id)
                elif r_sflag == 0:
                    tf1 = 1
                    tf2 = 1
                    new_entry = 'T'
                    print(cnt)
                    # ctime = (ctime - ((cnt+1)*20+endd))
                    ctime = ctime - end4
                    print(end4, ctime)
                    time.sleep(ctime)



            elif ((tf1 == 0) and (new_entry == 'E')) or ((tf2 == 0) and (new_entry == 'E')):  ###exit and entry
                start_time5 = timeit.default_timer()
                tws.cancelOrder(order_id)
                order_id = callback.next_ValidId + 1
                callback.next_ValidId = order_id
                qty = ps_qty
                o_type = "MKT"
                order_info = create.create_order(ctrct[8], o_type, qty, signal, price, True)
                tws.placeOrder(order_id, contract_info, order_info)
                time.sleep(1)
                fetchexe(order_id)
                # write to csv
                r_sflag, cnt, r_qty = entryfun(signal, price)
                end5 = timeit.default_timer() - start_time5
                if r_sflag == 1:
                    s_qty = r_qty  ####qty from the market order inside the function entryfun()
                    # time.sleep(1)
                    ctime = (ctime - end5)
                    print(end5, ctime)
                    time.sleep(ctime)
                    fetchexe(order_id)
                    # write into csv
                elif r_sflag == 0:
                    tf1 = 1
                    tf2 = 1
                    new_entry = 'T'
                    # ctime = ((ctime-1)-((cnt+1)*20+ende))
                    ctime = ctime - end5
                    print(end5, ctime)
                    time.sleep(ctime)

                    # partial fill
        elif (0 < filled < qty) and (remain > 0):

            fetchexe(order_id)
            # write into csv
            if ((tf1 == 1) and (new_entry == 'T')) or ((tf2 == 1) and (new_entry == 'T')):  # exit
                start_time6 = timeit.default_timer()
                qty = remain
                o_type = "MKT"
                order_id = callback.next_ValidId + 1
                callback.next_ValidId = order_id
                order_info = create.create_order(ctrct[8], o_type, qty, signal, price, True)
                tws.placeOrder(order_id, contract_info, order_info)
                end6 = timeit.default_timer() - start_time6
                # to be written in csv ,do not re write the existing price variable
                ctime = ctime - end6
                print(end6, ctime)
                time.sleep(ctime)
                fetchexe(order_id)

            elif ((tf1 == 0) and (new_entry == 'F')) or ((tf2 == 0) and (new_entry == 'F')):  ###entry
                start_time7 = timeit.default_timer()
                r_sflag, cnt, r_qty = entryfun(signal, price)
                end7 = timeit.default_timer() - start_time7
                if r_sflag == 1:
                    s_qty = filled + r_qty  ###qty from the market order in the entryfun
                    # ctime = ((ctime - 1) - (cnt * 20))
                    ctime = ctime - end7
                    print(end7, ctime)
                    time.sleep(ctime)
                    fetchexe(order_id)
                    # write into csv
                elif r_sflag == 0:
                    s_qty = filled
                    # ctime = (ctime  - ((cnt+1) * 20))
                    ctime = ctime - end7
                    print(end7, ctime)
                    time.sleep(ctime)
            elif ((tf1 == 0) and (new_entry == 'E')) or ((tf2 == 0) and (new_entry == 'E')):  ###exit and entry
                if (filled < ps_qty):
                    start_time8 = timeit.default_timer()
                    qty = (ps_qty - filled)
                    o_type = "MKT"
                    order_id = callback.next_ValidId + 1
                    callback.next_ValidId = order_id
                    order_info = create.create_order(ctrct[8], o_type, qty, signal, price, True)
                    tws.placeOrder(order_id, contract_info, order_info)
                    time.sleep(1)
                    fetchexe(order_id)
                    # write into csv
                    r_sflag, cnt, r_qty = entryfun(signal, price)
                    end8 = timeit.default_timer() - start_time8
                    if r_sflag == 1:
                        s_qty = r_qty  ###frm the market order inside the entry function
                        # ctime = ((ctime - 2) - (cnt * 20))
                        ctime = ctime - end8
                        print(end8, ctime)
                        time.sleep(ctime)
                        fetchexe(order_id)
                        # write into csv
                    elif r_sflag == 0:
                        tf1 = 1
                        tf2 = 1
                        new_entry = 'T'
                        # ctime = ((ctime - 1) - ((cnt+1) * 20))
                        ctime = ctime - end8
                        print(end8, ctime)
                        time.sleep(ctime)



                elif (filled > ps_qty):
                    start_time9 = timeit.default_timer()
                    r_sflag, cnt, r_qty = entryfun(signal, price)
                    end9 = timeit.default_timer() - start_time9
                    if r_sflag == 1:
                        s_qty = r_qty + (filled - ps_qty)  ##qty is the qty from mkt orfer inside the entryfun
                        # ctime = ((ctime - 1) - (cnt * 20))
                        ctime = ctime - end9
                        print(end9, ctime)
                        time.sleep(ctime)
                        fetchexe(order_id)
                        # write into csv
                    elif r_sflag == 0:
                        s_qty = (filled - ps_qty)
                        # ctime = ctime - ((cnt+1) * 20)
                        ctime = ctime - end9
                        print(end9, ctime)
                        time.sleep(ctime)
                elif (filled == ps_qty):
                    start_time10 = timeit.default_timer()
                    r_sflag, cnt, r_qty = entryfun(signal, price)
                    end10 = timeit.default_timer() - start_time10
                    if r_sflag == 1:
                        s_qty = r_qty  ##qty is the qty from mkt orfer inside the entryfun
                        # ctime = ((ctime-1) - (cnt * 20))
                        ctime = ctime - end10
                        time.sleep(ctime)
                        print(end10, ctime)
                        fetchexe(order_id)
                        # write into csv
                    elif r_sflag == 0:
                        tf1 = 1
                        tf2 = 1
                        new_entry = 'T'
                        # ctime = ctime - ((cnt+1) * 20)
                        ctime = ctime - end10
                        print(end10, ctime)
                        time.sleep(ctime)

    elif (i == (times - 1)):
        if (tf1 == 0) or (tf2 == 0):
            if (signal == 'BUY'):
                o_type = 'MKT'
                signal = 'SELL'
                qty = s_qty
                order_id = callback.next_ValidId + 1
                callback.next_ValidId = order_id
                order_info = create.create_order(ctrct[8], o_type, qty, signal, price, True)
                tws.placeOrder(order_id, contract_info, order_info)
                time.sleep(1)
                fetchexe(order_id)
            elif (signal == 'SELL'):
                o_type = 'MKT'
                signal = 'BUY'
                qty = s_qty
                order_id = callback.next_ValidId + 1
                callback.next_ValidId = order_id
                order_info = create.create_order(ctrct[8], o_type, qty, signal, price, True)
                tws.placeOrder(order_id, contract_info, order_info)
                time.sleep(1)
                fetchexe(order_id)





