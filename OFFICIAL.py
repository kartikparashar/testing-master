from tkinter import*
import time
from IBWrapper import IBWrapper,contract
from ib.ext.EClientSocket import EClientSocket
import pandas as pd
from datetime import datetime
import os
from tkinter import ttk
import getpass
import tkinter.filedialog


#import tkMessageBox
root = Tk()
user = getpass.getuser()

root.configure(background='black')
root.title('HISTORICAL DATA - TWS_MNS')
#TWS paramters for connectivity
callback = IBWrapper()
tws = EClientSocket(callback)
host = ""
port = 7497
clientId = 100
#accountName = "U1918033"



def getdata():
    # ticker
    global tick
    global mySymbol
    global optionmenus
    mySymbol = tick.get()
    # type
    global box_value
    global type
    type = box_value.get()
    #EXCHANGE
    global box_value2
    global exch1
    exch1=box_value2.get()
    # currency
    global box_value3
    global cur
    cur = box_value3.get()
    #enddate
    global box_value11
    global yr1
    yr1=box_value11.get()

    global box_value12
    global yr2
    yr2=box_value12.get()

    global box_value13
    global yr3
    yr3=box_value13.get()

    global yr4
    yr4=yr1+yr2+yr3+" "

    global yr5
    yr5="12:00:00"+" "+"IST"

    global yr6
    yr6=yr4+yr5



    #expiry

    global box_value14
    global exp1
    exp1 = box_value14.get()

    global box_value15
    global exp2
    exp2 = box_value15.get()

    global box_value16
    global exp3
    exp3 = box_value16.get()

    global exp4
    exp4 = exp1 + exp2 + exp3




    #multiplier
    global multp
    global multi
    multi=multp.get()
    #fetch data for
    global bar1
    global bar2
    bar2=bar1.get()

    global box_value4
    global bar3
    bar3=box_value4.get()

    global bardat
    bardat=bar2+" "+bar3

    #barsize

    global box_value5
    global bar4
    bar4= box_value5.get()


    #directory
    global box_value6
    global ent

    global pat
    pat=box_value6.get()

    global pat2
    pat2=ent.get()

    global pat3

    pat3=pat+pat2












    create = contract()
    callback.initiate_variables()




    # calling historical_Data attribute from intiate_variable function under IBWrapper class

    print("Testing Historical Data\n")

    contract_Details1 = create.create_contract(mySymbol, type, exch1, cur,'','',exp4,multi) #"", "",
                                               #"20170317",
                                               #"50")  # ('NG', 'FUT', 'NYMEX', 'USD')
    data_endtime = datetime.now().strftime("%Y%m%d %H:%M:%S")

    tws.reqHistoricalData(9000, contract_Details1, yr6,
                          bardat, bar4, "TRADES", 0, 1)
    time.sleep(1)
    data = pd.DataFrame(callback.historical_Data,
                        columns=["reqId", "date", "open",
                                 "high", "low", "close",
                                 "volume", "count", "WAP",
                                 "hasGaps"])
    dat=data.drop(data.index[len(data) - 1])
    base_dir = pat3
    global fname
    global ffname
    ffname = fname.get()
    filename = ffname + '.csv'
    #filename = mySymbol + '.csv'
    dat.to_csv(os.path.join(base_dir, filename))

def connect():
    tws.eConnect(host, port, clientId)
    print("connected")


def DISCONNECT():
        time.sleep(2)
        tws.eDisconnect()
        print("disconnected")





# Our state variables for the app
cvt_from = StringVar()
cvt_to = StringVar()
#connection
con= Label(root,text='CONNECT/DISCONNECT TWS',fg='orange',bg='black')
con.grid(row=0, column=0, columnspan=1)
lbl = Label(root,text=' INPUT PARAMETERS',fg='orange',bg='black')
lbl.grid(row=2, column=0, columnspan=1)
connect_btn = Button(root,fg='green',bg='snow',
 text='CONNECT!', command=connect)
connect_btn.grid(row=1, column=0)
#disconnect
disconnect_btn = Button(root,text='DISCONNECT!',fg='tomato',bg='snow', command=DISCONNECT)
disconnect_btn.grid(row=1, column=1)
#ticker
TICKER = Label(root,bg='black',fg='white', text='TICKER')
TICKER.grid(row=3, column=0)
tick = Entry(root)
tick.grid(row=3 , column=1)
#TYPE
type = Label(root,bg='black',fg='white', text='TYPE')
type.grid(row=4, column=0)
box_value = StringVar()
box1 = ttk.Combobox(root, textvariable=box_value,
                        state='normal')
box1['values'] = ('STK', 'FUT','CUR','COMMODITY')
box1.current(0)
box1.grid(column=1, row=4)
#exchange
type = Label(root,bg='black',fg='white', text='EXCHANGE')
type.grid(row=5, column=0)
box_value2 = StringVar()
box2 = ttk.Combobox(root, textvariable=box_value2,
                        state='normal')
box2['values'] = ('SMART', 'GLOBEX','NYMEX')
box2.current(0)
box2.grid(column=1, row=5)
#CURRENCY
type = Label(root,bg='black',fg='white', text='CURRENCY')
type.grid(row=6, column=0)
box_value3 = StringVar()
box3 = ttk.Combobox(root, textvariable=box_value3,
                        state='normal')
box3['values'] = ('USD', '','')
box3.current(0)
box3.grid(column=1, row=6)
#enddate
end = Label(root,bg='black',fg='white', text='END DATE')
end2 = Label(root,bg='black',fg='firebrick1', text='(FORMAT:YYMMDD)')
end.grid(row=7, column=0)
end2.grid(row=7,column=5)

box_value11 = StringVar()
box11 = ttk.Combobox(root, textvariable=box_value11,
                        state='normal')
box11['values'] = ('1990' ,'1991','1992','1993','1994','1995','1996','1997','1998','1999','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017')
box11.current(27)
box11.grid(column=1, row=7)  #box_value11

box_value12= StringVar()
box12 = ttk.Combobox(root, textvariable=box_value12,
                        state='normal')
box12['values'] = ('01', '02','03','04','05','06','07','08','09','10','11','12')
box12.current(0)
box12.grid(column=2, row=7)  #box_value12


box_value13= StringVar()
box13= ttk.Combobox(root, textvariable=box_value13,
                        state='normal')
box13['values'] = ('01', '02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31')
box13.current(0)
box13.grid(column=3, row=7)  #box_value13
#expiry
exp = Label(root,bg='black',fg='white', text='EXPIRY')
exp.grid(row=9, column=0)
exp12 = Label(root,bg='black',fg='firebrick1', text='(FORMAT:YYMMDD)')
exp12.grid(row=9, column=5)
box_value14 = StringVar()
box14 = ttk.Combobox(root, textvariable=box_value14,
                        state='normal')
box14['values'] = ('','1990' ,'1991','1992','1993','1994','1995','1996','1997','1998','1999','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019')
box14.current(0)
box14.grid(column=1, row=9)  #box_value14

box_value15= StringVar()
box15 = ttk.Combobox(root, textvariable=box_value15,
                        state='normal')
box15['values'] = ('','01', '02','03','04','05','06','07','08','09','10','11','12')
box15.current(0)
box15.grid(column=2, row=9)  #box_value15


box_value16= StringVar()
box16= ttk.Combobox(root, textvariable=box_value16,
                        state='normal')
box16['values'] = ('','01', '02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31')
box16.current(0)
box16.grid(column=3, row=9)  #box_value16

#multiplier
mult= Label(root,bg='black',fg='white', text='MULTIPLIER')
mult.grid(row=11, column=0)
multp = Entry(root)
multp.grid(row=11, column=1)
#fetch data for
bar= Label(root,bg='black',fg='white', text='FETCH DATA FOR')
bar.grid(row=12, column=0)
bar1 = Entry(root)
bar1.grid(row=12, column=1)   #bar1

box_value4 = StringVar()
box4 = ttk.Combobox(root, textvariable=box_value4,
                        state='normal')
box4['values'] = ('D','W','M','Y')
box4.current(0)
box4.grid(column=2, row=12) #box_value4
#barsize
siz= Label(root,bg='black',fg='white', text='DATA SIZE')
siz.grid(row=13, column=0)
#siz1 = Entry(root)
#siz1.grid(row=13, column=1)   #siz1

box_value5 = StringVar()
box5 = ttk.Combobox(root, textvariable=box_value5,
                        state='normal')
box5['values'] = (#'1 secs', '5 secs', '10 secs', '15 secs', '30 secs', '1 min', '2 mins', '3 mins', '5 mins', '10 mins', '15 mins', '20 mins', '30 mins',
     '1 hour', '2 hours', '3 hours', '4 hours', '8 hours', '1 day', '1W', '1M')
box5.current(0)
box5.grid(column=1, row=13) #box_value5

#empty rows and columns
x= Label(root,bg='black',fg='white', text='')
x.grid(row=15, column=3)
x1= Label(root,bg='black',fg='white', text='')
x1.grid(row=16, column=3)
x2= Label(root,bg='black',fg='white', text='')
x2.grid(row=17, column=3)
x3= Label(root,bg='black',fg='white', text='')
x3.grid(row=18, column=3)


#path

filename= Label(root,bg='black',fg='white', text='FILE NAME')
filename.grid(row=19,column=0)
fname = Entry(root)
fname.grid(row=19, column=1)

x5= Label(root,bg='black',fg='white', text='CHOOSE DIRECTORY')
x6= Label(root,bg='black',fg='firebrick1', text='NOTE:{REPLACE "/" WITH "//" OR "\ " if the sub-folders are mentioned }')
x5.grid(row=20, column=0)
x6.grid(row=21, column=5)
box_value6 = StringVar()
box6 = ttk.Combobox(root, textvariable=box_value6,
                        state='normal')
box6['values'] = (("D:/", "C:/ ", "E:/ "))
box6.current(0)
box6.grid(column=1, row=20) #box_value5
ent = Entry(root)
ent.grid(row=20, column=2)












but3 = Button(root, text="SUBMIT/FETCH DATA", fg="white", bg='orange', command=getdata)
but3.grid(row=21,column=1)




root.mainloop()
