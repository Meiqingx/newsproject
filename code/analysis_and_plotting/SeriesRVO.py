
import AR_model
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from matplotlib.pylab import rcParams
import datetime
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.arima_model import ARIMA


class Series:

    def __init__(self, file):
        '''
        Construct a new model to predict prices
        '''
        self._file = file
        self._table = self._create_pandas(self._file)


    def _create_pandas(self,file):
        '''
        Creates a dataframe with adequate characteristics for time series 
        analysis

        Inputs:
            file = name of the file

        Outputs:
            dataframe
        '''

        dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m')
        # from https://www.analyticsvidhya.com/blog/2016/02/time-series-forecasting-codes-python/

        database = pd.read_csv(file, parse_dates=['Date'], index_col='Date',
            date_parser=dateparse)
        database = database.dropna(axis=1)

        original_columns = list(database.dtypes.index)

        for series_name in database.dtypes.index:
            new_name = series_name + "_sa"
            database[new_name] = seasonal_decompose(database[series_name], 
                freq=12).trend
            season_factor_name = series_name + "_season"

        database.drop(original_columns, axis = 1, inplace = True)
        database.sort_index(inplace=True)

        #self._table = database

        return database


    def descompose(series):
        '''
        Given a series, it splits in (trend, season, residual)

        Input:
            Series, a columns from a dataframe of the Series class

        Output:
            A tuple with (trend, seasonal, residual)
        '''
        split_variable = seasonal_decompose(series)
        trend = split_variable.trend
        seasonal = split_variable.seasonal
        residual = split_variable.resid

        return (trend, seasonal, residual)


    def print_seasonality(series):
        '''
        Given a series, generates a plot with trend, season, and residuals
        Idea and some code from:
        https://www.analyticsvidhya.com/blog/2016/02/time-series-forecasting-codes-python/

        Input:
            Series of a dataframe of the class Series

        Output:
            Graph
        '''
        trend, seasonal, residual = Series.descompose(series)
        plt.subplot(411)
        plt.plot(series, label='Original')
        plt.legend(loc='best')
        plt.subplot(412)
        plt.plot(trend, label='Trend')
        plt.legend(loc='best')
        plt.subplot(413)
        plt.plot(seasonal,label='Seasonality')
        plt.legend(loc='best')
        plt.subplot(414)
        plt.plot(residual, label='Residuals')
        plt.legend(loc='best')
        plt.tight_layout()

        return plt.show()

# This fuction is not in the class because it is useful for predictions, 
# not of the characteristics of the series. However, we believe this is 
# a better place for it than in the file Predict.py

def series_for_prediction(independent_vars, num_years_to_predict):
    '''
    Creates a dataframe with future values for the independent variables

    Inputs:
        independent_vars = dataframe with original independent variables
        num_year_to_predict = integer

    Outputs:
        result = dataframe with original and predicted values for the 
            independent variables
    '''
    new_independent_series = []
    variables = list(independent_vars.columns)
    for name in list(independent_vars.columns):
        one_series = independent_vars[name]
        X, predictions, integrated = AR_model.AR_independent_vars(one_series, 
            num_years_to_predict)
        new_independent_series.append(integrated)

    result = pd.concat(new_independent_series, axis=1)
    result.columns = variables

    return result
