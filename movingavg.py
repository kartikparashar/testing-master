from tkinter import*
import datetime
from IBWrapper import IBWrapper,contract
from ib.ext.EClientSocket import EClientSocket
import pandas as pd
from datetime import datetime
import os
from tkinter import ttk
import getpass
import tkinter.filedialog
import tkinter as tk
import matplotlib
import numpy as np
import csv
import pandas as pd

# import tkMessageBox
root3 = Tk()


root3.configure(background='black')
root3.title('MOVING AVERAGE - TWS_MNS')
# TWS paramters for connectivity





def meancalculate():
        global entmean11
        global entm
        global entm1
        entm1 = entmean11.get()
        #entm=print(entm1)


        global box_mean
        global box_meanval
        box_meanval = box_mean.get()

        global entmean1
        global mfile
        mfile = entmean1.get()

        # directory
        global box_value6
        global ent

        global pat
        pat = box_value6.get()

        global pat2
        pat2 = ent.get()

        global pat3

        pat3 = pat+pat2



        global meanfile
        meanfile = box_meanval+mfile+'.csv'




        meanfinal = pd.read_csv(meanfile)
        meanfinal = meanfinal.replace('[]', np.nan)

        meanfinal.dropna(how='any', inplace=True)



        b=pd.rolling_mean(meanfinal["close"],int(entm1))

        #b = pd.rolling_mean(meanfinal["close"],int(entm1))
        b = pd.DataFrame(b)



        global rename
        rename=entm1 +'day MovingAvg'
        b = b.rename(columns={'close': rename})
        new = pd.concat([meanfinal, b], axis=1)
        #print(new)


        #new.iloc[2:-1].plot(y='close')

        #new.plot(x="date")#,y="close")#,secondary_y="rename")





        global fname
        global ffname
        base_dir = pat3
        ffname = fname.get()
        filename = ffname+'.csv'
        new.to_csv(os.path.join(base_dir, filename))

        df = pd.read_csv(base_dir+filename)

        df = df.replace('[]', np.nan)

        df.dropna(how='any', inplace=True)
        dp = df.drop(df.columns[[0]], axis=1)

        base_dir = pat3
        ffname = fname.get()
        filename = ffname + '.csv'
        dp.to_csv(os.path.join(base_dir, filename))

        dp.iloc[2:-1].plot(x='date')
        #df.plot(x='date')
        print(dp)











mean= Label(root3,bg='black',fg='orange', text='GET MOVING AVERAGE',font='VERONICA')
mean.grid(row=0,column=0)


mean = Label(root3, bg='black', fg='white', text='GET MOVING AVERAGE FROM EXISTING DATA FILE')
mean.grid(row=5, column=0)









box_mean = StringVar()
boxmean = ttk.Combobox(root3, textvariable=box_mean,
                state='normal')
boxmean['values'] = (("D:/", "C:/ ", "E:/ "))
boxmean.current(0)
boxmean.grid(column=1, row=5) #box_value5
entmean1 = Entry(root3)
entmean1.grid(row=5, column=2)



meanent1= Label(root3,bg='black',fg='white', text='ENTER MOVING AVERAGE ')
meanent1.grid(row=6,column=0)
entmean11 = Entry(root3)
entmean11.grid(row=6, column=1)



xs= Label(root3,bg='black',fg='ORANGE', text='SAVE FILE',font='VERONICA')
xs.grid(row=8, column=0)


filename= Label(root3,bg='black',fg='white', text='FILE NAME')
filename.grid(row=19,column=0)
fname = Entry(root3)
fname.grid(row=19, column=1)

x5= Label(root3,bg='black',fg='white', text='CHOOSE DIRECTORY')
x6= Label(root3,bg='black',fg='firebrick1', text='NOTE:{REPLACE "/" WITH "//" OR "\ " if the sub-folders are mentioned }')
x5.grid(row=20, column=0)
x6.grid(row=21, column=5)
box_value6 = StringVar()
box6 = ttk.Combobox(root3, textvariable=box_value6,
                        state='normal')
box6['values'] = (("D:/", "C:/ ", "E:/ "))
box6.current(0)
box6.grid(column=1, row=20) #box_value5
ent = Entry(root3)
ent.grid(row=20, column=2)

newmean11 = Button(root3, text="FETCH MOVING AVERAGE AND PLOT", fg="white", bg='red', command=meancalculate)
newmean11.grid(row=24, column=1)



root3.mainloop()