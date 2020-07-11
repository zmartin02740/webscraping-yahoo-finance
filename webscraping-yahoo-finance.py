#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import pandas as pd


# In[27]:


tickers = ['AAPL', 'MSFT']
financial_dir = {}

for ticker in tickers:
    temp_dir = {}
    url = 'https://in.finance.yahoo.com/quote/' + ticker + '/balance-sheet?p=' + ticker
    page = requests.get(url)
    page_content = page.content
    soup = BeautifulSoup(page_content, 'html.parser')
    tabl = soup.find_all('div', {'class': 'M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)'})
    for t in tabl:
        rows = t.find_all('div', {'class': 'rw-expnded'})
        for row in rows:
            temp_dir[row.get_text(separator='|').split('|')[0]] = row.get_text(separator='|').split('|')[1]
            
    url = 'https://in.finance.yahoo.com/quote/' + ticker + '/financials?p=' + ticker
    page = requests.get(url)
    page_content = page.content
    soup = BeautifulSoup(page_content, 'html.parser')
    tabl = soup.find_all('div', {'class' : 'M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)'})
    for t in tabl:
        rows = t.find_all('div', {'class': 'rw-expnded'})
        for row in rows:
            temp_dir[row.get_text(separator='|').split('|')[0]] = row.get_text(separator='|').split('|')[1]
    
    url = 'https://in.finance.yahoo.com/quote/' + ticker + '/cash-flow?p=' + ticker
    page = requests.get(url)
    page_content = page.content
    soup = BeautifulSoup(page_content, 'html.parser')
    tabl = soup.find_all('div', {'class' : 'M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)'})
    for t in tabl:
        rows = t.find_all('div', {'class': 'rw-expnded'})
        for row in rows:
            temp_dir[row.get_text(separator='|').split('|')[0]] = row.get_text(separator='|').split('|')[1]
    
    url = 'https://in.finance.yahoo.com/quote/'+ ticker + '/key-statistics?p=' + ticker
    page = requests.get(url)
    page_content = page.content
    soup = BeautifulSoup(page_content, 'html.parser')
    tabl = soup.findAll('div', {'class': 'Mstart(a) Mend(a)'})
    for t in tabl:
        rows = t.find_all('div')
        if len(row.get_text(separator='|').split('|')[0:2])>0:
            temp_dir[row.get_text(separator='|').split('|')[0]] = row.get_text(separator='|').split('|')[1]
    financial_dir[ticker] = temp_dir

combined_financials = pd.DataFrame(financial_dir)
tickers = combined_financials.columns
for ticker in tickers:
    combined_financials = combined_financials[~combined_financials[ticker].str.contains('[a-z]').fillna(False)]
print(combined_financials)


# In[ ]:




