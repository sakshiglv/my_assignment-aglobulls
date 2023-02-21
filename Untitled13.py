#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install alpha_vantage


# In[2]:


##importing pandas and numpy module
import pandas as pd
import numpy as np
from alpha_vantage.timeseries import TimeSeries


# In[3]:


##creating a 'ScriptData' class alongwith two methods ,'fetch_intraday_data' and 'convert_intraday_data'

class ScriptData:
    def fetch_intraday_data(self,script):
        API_key = '7NYR4A1375NJJLH0'

        ts = TimeSeries(key = API_key)
        data , meta = ts.get_intraday(script)
        
        return data
        
    def  convert_intraday_data(self,script):
        data = self.fetch_intraday_data(script)
        simplifiedData = {}
        rowCount=0
        for key, value in data.items():
            simplifiedData[rowCount] = {}    
            simplifiedData[rowCount]['timestamp']=key
            simplifiedData[rowCount]['open']=value['1. open']
            simplifiedData[rowCount]['high']=value['2. high']
            simplifiedData[rowCount]['low']=value['3. low']
            simplifiedData[rowCount]['close']=value['4. close']
            simplifiedData[rowCount]['volume']=value['5. volume']
            rowCount+=1

        df= pd.DataFrame.from_dict(simplifiedData,orient = 'index')
        return df
    
    def indicator1(self,dataframe,timeperiod=5):
        dataframe['indicator'] = dataframe['close'].rolling(window = timeperiod).mean().round(4)
        
        ddf =  dataframe[['timestamp','indicator']]
        
        return ddf

        
        


# In[4]:


##  sample code-1
di = ScriptData()
a = di.convert_intraday_data('GOOGL')
di.indicator1(a,5)




# In[5]:


## creating another class 'Strategy' alongwith two mehods 'get_script_data' and 'get_signals'

class Strategy:
    def __init__(self,script):
        self.script_data = ScriptData()
        self.script = script
    
    
    def get_script_data(self):
        b = self.script_data.convert_intraday_data(self.script)
        c = self.script_data.indicator1(b)
        b.indicator = c.indicator
        b.rename(columns={'close':'close_data','indicator':'indicator_data'},inplace=True)
        
        return b
    
    def get_signals(self):
        E = self.get_script_data()
        for i in range(1 ,E.shape[0]):
            if  (E['indicator_data'][i-1] >= E['indicator_data'][i]) and (E['close_data'][i-1] <= E['close_data'][i]):
                E.loc[i,'signal'] = 'SELL'
            elif  (E['indicator_data'][i-1] <= E['indicator_data'][i]) and (E['close_data'][i-1] >= E['close_data'][i]):
                E.loc[i,'signal'] = 'BUY'
            else:
                E.loc[i,'signal'] = 'NO_SIGNAL'        
        df1 = E[['timestamp','signal']]
        return df1.loc[(E['signal']=='BUY')|(E['signal']=='SELL')]
        

        
        
        


# In[7]:


##sample code-2

dE = Strategy('GOOGL')
dE.get_script_data()
dE.get_signals()

