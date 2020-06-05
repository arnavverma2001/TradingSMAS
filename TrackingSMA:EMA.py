import robin_stocks as r
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from datetime import datetime
key = ""
ts = TimeSeries(key, output_format='pandas')
ti = TechIndicators(key, output_format='pandas')

r.login()

mystocks = r.build_holdings()


dataframe = pd.DataFrame(mystocks)
dataframe = dataframe.T
dataframe["ticker"] = dataframe.index
dataframe = dataframe.reset_index(drop=True)
cols = dataframe.columns.drop(['id','type','name','pe_ratio','ticker'])
dataframe[cols] = dataframe[cols].apply(pd.to_numeric, errors='coerce')
dataframe.to_excel("stocks.xlsx","StockHoldings")

stockticker = "F"

data_ts, meta_data_ts = ts.get_intraday(stockticker, interval = '1min', outputsize = 'full')

period = 60

sma_ti, meta_sma_ti = ti.get_sma(stockticker, interval = '1min', time_period = period, series_type = 'close')
ema_ti, meta_ema_ti = ti.get_ema(stockticker, interval = '1min', time_period = period, series_type = 'close')


data1 = sma_ti
data2 = data_ts['4. close'].iloc[period-1::]
data3 = ema_ti

totaldata = pd.concat([data1,data2,data3], axis=1)
rows = totaldata.shape[0]
totaldata = totaldata.iloc[rows - 376:rows]                           
print(totaldata)
totaldata.plot()
plt.show()
