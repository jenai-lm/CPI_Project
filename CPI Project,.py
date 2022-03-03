#!/usr/bin/env python
# coding: utf-8

# In[117]:


import requests
import json
import pandas as pd
get_ipython().run_line_magic('run', 'APIkeys.py')
key = os.environ['BLS_API_key']
def multiSeriesV4(varList,myKey):
    # Input: varList = a list of strings containing the series names
    # Input: myKey =  a string containing your BLS API key
    # Output: new_df = a data frame containing the data collected
    
    base_url = 'https://api.bls.gov/publicAPI/v2/timeseries/data/'  #this will not change
    headers = {'Content-type': 'application/json'}  #This will not changed !

    parameters = {
        "seriesid":varList,
        "startyear":"2017", 
        "endyear":"2022",
        "catalog":True, 
        "calculations":False, 
        "annualaverage":False,
        "aspects":False,
        "registrationkey": myKey 
     }

    data = json.dumps(parameters) #this converts the Python dictionary into a JSON format
    
    p = requests.post(base_url, data=data, headers=headers)
    json_data = json.loads(p.text)
    
    n = len(varList) #number of series requested
    
    new_df = pd.DataFrame(columns=['year', 'period'])
    for item in range(n):
        l = len(json_data['Results']['series'][item]['data']) #length of the list
        if l == 0:
            print('Series ',varList[item],' does not exist')
        else:
            
            print('Series ',varList[item],' exists with ',l,' observations')
            d = json_data['Results']['series'][item]['data']
            current_df = pd.DataFrame(data=d)
            current_df = current_df[['year','period','value']].astype({'value': 'float64'})
            current_df = current_df.rename(columns = {'value':varList[item]})
            new_df = new_df.merge(current_df, on = ['year','period'],how='outer')
    
    return new_df


# In[118]:


#check to make sure that all items exist in south
basket = ['CUUR0300SEFV', 'CUUR0300SAF116', 'CUUR0300SETA02', 'CUUR0300SETB01', 'CUUR0300SAA', 'CUUR0300SARC', 'CUUR0300SARS', 'CUUR0300SAM'
]


# In[119]:


south = multiSeriesV4(basket, key)


# In[133]:


#add weights to items in basket
south['CPISouth']= 0.12*south['CUUR0300SARS'] + 0.12*south['CUUR0300SARC'] + 0.184*south['CUUR0300SAM'] + 0.125*south['CUUR0300SEFV'] + 0.085*south['CUUR0300SAF116'] + 0.046*south['CUUR0300SAA'] + 0.133*south['CUUR0300SETB01'] + 0.1877*south['CUUR0300SETA02']
south


# In[124]:


#check to make sure all items are available in the northeast
basket = ['CUUR0100SEFV', 'CUUR0100SAF116', 'CUUR0100SETA02', 'CUUR0100SETB01', 'CUUR0100SAA', 'CUUR0100SARC', 'CUUR0100SARS', 'CUUR0100SAM'
]


# In[125]:


northe = multiSeriesV4(basket, key)


# In[127]:


# add weights to items in northeast basket
northe['CPINorthE']= 0.12*northe['CUUR0100SARS'] + 0.12*northe['CUUR0100SARC'] + 0.184*northe['CUUR0100SAM'] + 0.125*northe['CUUR0100SEFV'] + 0.085*northe['CUUR0100SAF116'] + 0.046*northe['CUUR0100SAA'] + 0.133*northe['CUUR0100SETB01']
northe


# In[128]:


basket = ['CUUR0400SEFV', 'CUUR0400SAF116', 'CUUR0400SETA02', 'CUUR0400SETB01', 'CUUR0400SAA', 'CUUR0400SARC', 'CUUR0400SARS', 'CUUR0400SAM'
]


# In[129]:


#check items in the west are available
west = multiSeriesV4(basket, key)


# In[134]:


#add weights to items in west basket
west['CPIWest']= 0.12*west['CUUR0400SARS'] + 0.12*west['CUUR0400SARC'] + 0.184*west['CUUR0400SAM'] + 0.125*west['CUUR0400SEFV'] + 0.085*west['CUUR0400SAF116'] + 0.046*west['CUUR0400SAA'] + 0.133*west['CUUR0400SETB01']
west


# In[135]:


#finalizing the basket of goods, regions are weighted evenly 
allregions = 0.33*west['CPIWest'] + 0.33*northe['CPINorthE'] + 0.34*south['CPISouth']
allregions

