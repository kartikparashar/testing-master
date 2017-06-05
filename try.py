

import pandas as pd
import numpy as np


df = pd.read_csv('E:\gggg.csv')
meanfinal=df

meanfinal = meanfinal.replace('[]', np.nan)

meanfinal.dropna(how='any', inplace=True)
ma=5
b = pd.rolling_mean(meanfinal["close"], int(ma))

b = pd.DataFrame(b)
global rename
rename =  "%s"%ma + 'day MovingAvg'
b = b.rename(columns={'close': rename})
new = pd.concat([meanfinal, b], axis=1)


df = new.replace('[]', np.nan)

df.dropna(how='any', inplace=True)
dp = df.drop(df.columns[[0]], axis=1)





