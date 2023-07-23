#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd
import numpy as np
from pandas import json_normalize
import datetime
import os

import warnings
warnings.filterwarnings("ignore")


# In[2]:


# request api

response = requests.get("https://api.weather.gov/products/types/TOR")
data = response.json()


# In[3]:


# normalize data

norm_data = json_normalize(data)
norm_data = json_normalize(norm_data['@graph']).T.set_axis(['series'], axis=1)#, inplace=False)
norm_data = norm_data['series'].apply(pd.Series)


# In[4]:


# get additional information about event

def get_id_info(id):
    response = requests.get(id)
    norm_data2 = response.json()
    id2 = norm_data2['@id']
    wmoCollectiveId = norm_data2['wmoCollectiveId']
    issuingOffice = norm_data2['issuingOffice']
    issuanceTime = norm_data2['issuanceTime']
    productCode = norm_data2['productCode']
    productName = norm_data2['productName']
    productText = norm_data2['productText']
    event_info = [id2, wmoCollectiveId, issuingOffice, issuanceTime, productCode, productName, productText]
    return event_info


# In[5]:


# append new info to df

newdata = []

for i in range(len(norm_data)):
    event2 = get_id_info(norm_data['@id'][i])
    newdata.append(event2)
    details = pd.DataFrame(newdata, columns = ['id2', 'wmoCollectiveId', 'issuingOffice', 'issuanceTime', 'productCode', 'productName', 'productText'])


# In[6]:


# adjust format

def fix(text):
    text['productText'].replace("\n", " ")
    return text

details = fix(details)


# In[7]:


# create unique .csv titled with date

current_date = datetime.datetime.now()
filename = str(current_date.year) + str(current_date.month) + str(current_date.day)
#details.to_csv(str(filename + '.csv'))
os.makedirs('files', exist_ok = True)  
details.to_csv(str('files/' + filename + '.csv'), index = False)

