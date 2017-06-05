from IBWrapper import IBWrapper,contract
from ib.ext.EClientSocket import EClientSocket
import time
callback = IBWrapper()
tws = EClientSocket(callback)
host = ""
port = 7497
clientId = 100
tws.eConnect(host,port,clientId)


time.sleep(3)
#request ID 1
tws.reqIds(1)
order_id = callback.next_ValidId + 1


create = contract()
callback.initiate_variables()
time.sleep(3)
df=["AAPL", "STK", "SMART", "USD",'','','20170616','50',"DU228380","LMT","1","SELL","142.26"]
contract_info = create.create_contract(df[0],df[1],df[2],df[3])#,df[4],df[5],df[6],df[7])
order_info = create.create_order(df[8],df[9],df[10],df[11],df[12],True)


order_info2 = create.create_order(df[8],df[9],df[10],df[11],df[12],"143.26",True)


tws.placeOrder(order_id, contract_info, order_info)

tws.placeOrder(order_id, contract_info, order_info2)

