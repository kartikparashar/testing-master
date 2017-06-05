from ib.ext.Contract import Contract
from ib.ext.Order import Order
from ib.opt import Connection

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

import matplotlib.pyplot as plt
from ib.ext.EWrapper import EWrapper
from ib.ext.Contract import Contract
from ib.ext.ExecutionFilter import ExecutionFilter
from ib.ext.Order import Order

from random import randint



def error_handler(msg):

    print ("Server Error:", msg)




def server_handler(msg):

    print ("Server Msg:",msg.typeName, "-", msg)




def create_contract(symbol, sec_type, exch,curr):#exp,mul):

    contract = Contract()

    contract.m_symbol = symbol

    contract.m_secType = sec_type

    contract.m_exchange = exch

    #contract.m_primaryExch = prim_exch

    contract.m_currency = curr

    #contract.m_expiry=exp
    #contract.m_multiplier=mul

    return contract




def create_order(order_type,lmtprice,quantity, action):

    order = Order()

    order.m_orderType = order_type

    order.m_lmtPrice=lmtprice

    order.m_totalQuantity = quantity

    order.m_action = action

    return order




if __name__ == "__main__":

    client_id = 100

    #order_id = 200121

    port = 7496



    tws_conn = None

    try:

# Establish connection to TWS.

        tws_conn = Connection.create(port=port,

        clientId=client_id)

        tws_conn.connect()




# Assign error handling function.

        tws_conn.register(error_handler, 'Error')




# Assign server messages handling function.

        tws_conn.registerAll(server_handler)




# Create AAPL contract and send order

        # = create_contract('GOOG','STK','SMART','USD')#'20170616',"50")
        df=['AAPL', 'STK', 'SMART', 'USD','MKT','100','20','SELL']

        strat1_contract = create_contract(df[0], df[1], df[2], df[3])



        #aapl_order = create_order('MKT',10000, 50, 'SELL')
        strat1_order = create_order(df[4], df[5], df[6], df[7])  # Go long 100 shares of AAPL

        callback = IBWrapper()
        tws = EClientSocket(callback)

        order_id=787986750
        if order_id==787986750:

            a=randint(787986750,999999999 )


        order_id=a



        tws_conn.placeOrder(order_id, strat1_contract, strat1_order)
        #tws_conn.placeOrder(order_id2, aapl_contract, aapl_order)




    finally:

# Disconnect from TWS

        if tws_conn is not None:

            tws_conn.disconnect()

            #tws.cancelOrder(order_id)