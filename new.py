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

import matplotlib.pyplot as plt
import arrow


callback = IBWrapper()
tws = EClientSocket(callback)
host = ""
port = 7497
clientId = 100

app=Flask(__name__)



@app.route('/')
def index():
    createLink ="<a href='" + url_for('conn') + "'> CONNECT</a>"
    return"""<html><body>"""+ createLink + """ </body></html>"""


@app.route('/conn')

def conn():

    tws.eConnect(host, port, clientId)
    print("connected")
    #createLink1 = "<a href='" + url_for('dis') + "'>DISCONNECT</a>"
    #return """<html><body>""" + createLink1 + """</body></html>"""
    return render_template('choose.html')


@app.route('/home')

def home():

    return render_template('home.html')


@app.route('/sma')
def sma():
    return render_template('moving average.html')

@app.route('/ticker' ,methods=['POST'])
def ticker():
    global ticker
    global type
    global exc
    global end
    global month
    global day
    global enddate
    global cur
    #ticker
    ticker = request.form['ticker']
    #type
    type=request.form['type']
    #exchange
    exc = request.form['exc']
    #endddate
    end=request.form['end']
    month=request.form['month']
    day=request.form['day']
    enddate= end+month+day+" "
    global yr5
    yr5 = "12:00:00" + " " + "IST"
    global enddate1
    enddate1=enddate+yr5

    #currency
    cur=request.form['cur']

 #expiry

    global end1,month1,day1,expiry
    end1=request.form['end1']
    month1=request.form['month1']
    day1=request.form['day1']
    expiry= end1+month1+day1

    #multiplier
    global mul
    mul=request.form['mul']


    #fetch data for
    global count,count1,fetch

    count=request.form['count']
    count1 = request.form['count1']
    fetch=count+" "+count1

    global ds
    ds=request.form['ds']

    global fname,dir,filesave
    fname=request.form['fname']
    dir = request.form['dir']

    filesave=dir+fname



    return render_template('output.html', ticker=ticker,type=type,exc=exc,enddate1=enddate1,cur=cur,expiry=expiry,mul=mul,ds=ds,
                           filesave=filesave)

@app.route('/dis')
def dis():
    tws.eDisconnect()
    print("disconnected")
    return"<h1>DISCONNECTED</h2>"

@app.route('/hist')
def hist():
    #print to console
    print("%s" %ticker )
    print("%s" %type)
    print("%s" %exc)
    print ("%s" %cur)
    print("%s" %enddate1)
    print("%s" %expiry)
    print("%s" %fetch)
    print("%s" %ds)

    #functionality

    #retrieve functions from other files

    create = contract()
    callback.initiate_variables()

    #fetch from TWS
    contract_Details1 = create.create_contract(ticker,type,exc,cur,'','',expiry,mul)#,'','',exp4,multi) #"", "",
                                               #"20170317",
                                               #"50")  # ('NG', 'FUT', 'NYMEX', 'USD')
    data_endtime = datetime.now().strftime("%Y%m%d %H:%M:%S")

    tws.reqHistoricalData(9000, contract_Details1,enddate1 ,
                          fetch,
                          ds,
                          "TRADES",
                          0,
                          1)
    time.sleep(1)
    data = pd.DataFrame(callback.historical_Data,
                        columns=["reqId", "date", "open",
                                 "high", "low", "close",
                                 "volume", "count", "WAP",
                                 "hasGaps"])

    #data['DateTime'] = data['date'].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))
    #data = data.drop('date', 1)

    #global dat
    #dat=data.drop(data.index[len(data) - 1])
    #print("%s" %data)

    df=data
    df[['DateTime']] = df[['date']].applymap(str).applymap(lambda s: "{}/{}/{} {}".format(s[0:4], s[4:6], s[6:8], s[8:]))

    data=df[["DateTime","close"]]

    print("%s" % data)

    base_dir = dir
    filename = fname + '.csv'
    data.to_csv(os.path.join(base_dir, filename))

    return render_template('trades.html', ticker=ticker, type=type, exc=exc, enddate1=enddate1, cur=cur,
                           expiry=expiry, mul=mul, ds=ds)
           # filesave=filesave)
           #return render_template('moving average.html', ticker=ticker,type=type,exc=exc,enddate1=enddate1,cur=cur,expiry=expiry,mul=mul,ds=ds,
                           #filesave=filesave)

@app.route('/moving' ,methods=['GET', 'POST'])
def moving():


    return render_template('movingavgg.html')



@app.route('/movingg' ,methods=['GET','POST'])
def movingg():
    global ma,fname1,dir,dp
    ma = request.form['ma']
    fname1 = request.form['fname1']
    dir1 = request.form['dir1']
    global meanfinal, meanfile
    meanfile = dir1 + fname1 + '.csv'

    meanfinal = pd.read_csv(meanfile)
    meanfinal = meanfinal.replace('[]', np.nan)
    meanfinal = pd.DataFrame(meanfinal)

    meanfinal['DateTime'] = meanfinal['date'].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))
    meanfinal = meanfinal.drop('date', 1)




    meanfinal.dropna(how='any', inplace=True)

    b = pd.rolling_mean(meanfinal["close"], int(ma))

    # b = pd.rolling_mean(meanfinal["close"],int(entm1))
    b = pd.DataFrame(b)

    rename = "MOVING_AVG"
    b = b.rename(columns={'close': rename})
    new = pd.concat([meanfinal, b], axis=1)

    # df = pd.read_csv(base_dir + filename)

    df = new.replace('[]', np.nan)

    df.dropna(how='any', inplace=True)
    dp = df.drop(df.columns[[0]], axis=1)
    print(dp)

    global dir2, fname2

    dir2 = request.form['dir2']
    fname2 = request.form['fname2']

    # base_dir = mfdir
    # ffname = mfname
    # filename = ffname + '.csv'

    filename1 =  fname2 +" "+ "%s" % ma + 'day MovingAvg'+'.csv'
    dp.to_csv(os.path.join(dir2, filename1))

    # dp.iloc[2:-1].plot(x='date')
    # df.plot(x='date')
    print(dp)






    return render_template("output2.html",ma=ma,dp=dp,dir1=dir1,dir2=dir2,fname1=fname1,fname2=fname2,rename=rename )#,ffname=ffname,dir1=dir1)

@app.route('/plot' ,methods=['GET','POST'])
def plot():

    global ax
    ax=pd.DataFrame(dp)
    yaxis1=request.form['yaxis1']
    yaxis2= request.form['yaxis2']
    b = ax[['DateTime',yaxis1,yaxis2]]
    b.plot(x='DateTime')
    figure_title= "%s" % ma + 'day MovingAvg'
    plt.title(figure_title)
    plt.show()


    return render_template('output 3.html')







if __name__ == "__main__":
    app.run(debug=True)
