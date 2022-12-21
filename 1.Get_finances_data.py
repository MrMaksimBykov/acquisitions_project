import pandas_datareader.data as web
from pandas_datareader import data as pdr
import yfinance as yf
from datetime import datetime


#DATEFROM = '1970-02-01'
#DATETO = '2022-11-01'
startdate = datetime(1970, 2, 1)
enddate = datetime(2022, 11, 1)
COMPANIES = {'AAPL': 'Apple', 'TWTR': 'Twitter', 'AMZN': 'Amazon', 'HPQ': 'Hp', 'GOOD': 'Google',
             'MSFT': 'Microsoft', 'BB': 'Blackberry', 'EBAY': 'Ebay', 'IBM': 'Ibm',
             'ADBE': 'Adobe', 'META': 'Facebook', 'DIS': 'Disney'}

yf.pdr_override()
df = pdr.get_data_yahoo(list(COMPANIES.keys()), start=startdate, end=enddate)
df_SP = pdr.get_data_yahoo('%5ESP500-45', start=startdate, end=enddate)

#df = web.DataReader(COMPANIES.keys(), 'yahoo', start=DATEFROM, end=DATETO)
#df_SP = web.DataReader('%5ESP500-45', 'yahoo', start=DATEFROM, end=DATETO)

cols = [col for col in df.columns if col[0] == 'Close']
df = df.loc[:, cols]
df.columns = [COMPANIES[col[1]] for col in cols]

df.to_csv('./DATA/companies.csv')
df_SP.to_csv('./DATA/S&P500.csv')
print(df)
print(df_SP)
