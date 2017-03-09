# Predicting Commodities Prices
# 2017 

'''
This file creates the necessary functions to analyse time series data 
'''

import pandas as pd

import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from matplotlib.pylab import rcParams
import datetime
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.arima_model import ARIMA

# Load the databases 

com_file = "/Users/ruy/Documents/UChicago/Winter_2017/cs/Project/newsproject/code/scrapers/commodities_data/commodities_prices.csv" 
gem_file = "/Users/ruy/Documents/UChicago/Winter_2017/cs/Project/newsproject/code/scrapers/worldbank/gem.csv"

commodities = pd.read_csv(com_file)
gem = pd.read_csv(gem_file)

dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m')
# data = pd.read_csv('AirPassengers.csv')

# data = pd.read_csv('AirPassengers.csv', parse_dates='Month', index_col='Month',date_parser=dateparse)
# print data.head()

commodities = pd.read_csv(com_file, parse_dates=['DATE'], index_col='DATE',date_parser=dateparse)

one_series = commodities['WLDBEEF']
two_series = commodities['WLDALUMINUM']
three_series = commodities['WLDCOPPER']
fourth_series = commodities['WLDSOYBEANS']

#################### ARIMA ######################

model = ARIMA(one_series, (2, 1, 1), exog = three_series, freq = 'M')

# First differences
one_series_diff = one_series - one_series.shift()
plt.plot(one_series_diff)

# Those are still in differences
results_ARIMA = model.fit(disp=-1)  
plt.plot(one_series_diff)
plt.plot(results_ARIMA.fittedvalues, color='red')
plt.title('RSS: %.4f'% sum((results_ARIMA.fittedvalues-one_series_diff)**2))
plt.show()

# Back to the original scale

predictions_ARIMA_diff = pd.Series(results_ARIMA.fittedvalues, copy=True)

predictions_ARIMA_diff_cumsum = predictions_ARIMA_diff.cumsum()

predictions_ARIMA_normal = pd.Series(one_series.ix[0], index=one_series.index)

predictions_ARIMA_normal = predictions_ARIMA_normal.add(predictions_ARIMA_diff_cumsum,fill_value=0)

predictions_ARIMA_normal.head()

plt.plot(one_series)
plt.plot(predictions_ARIMA_normal)
plt.show()



def test_stationarity(timeseries):
    
    #Determing rolling statistics
    rolmean = pd.rolling_mean(timeseries, window=12)
    rolstd = pd.rolling_std(timeseries, window=12)

    #Plot rolling statistics:
    orig = plt.plot(timeseries, color='blue',label='Original')
    mean = plt.plot(rolmean, color='red', label='Rolling Mean')
    std = plt.plot(rolstd, color='black', label = 'Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show(block=False)
    
    #Perform Dickey-Fuller test:
    print('Results of Dickey-Fuller Test:')
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print(dfoutput)


ts_log_decompose = residual
ts_log_decompose.dropna(inplace=True)
test_stationarity(ts_log_decompose)






