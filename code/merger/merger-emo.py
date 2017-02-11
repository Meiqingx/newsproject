import numpy as np
import pandas as pd
from datetime import datetime as dt



def read_files():
    '''
    '''


    precipitation_f = '../parsers/precipitation_means.csv'
    electricity_f = '../parsers/electricity_data.csv'
    recessions_f = '../parsers/recessions_data.csv'




    precip_hdrs = ['Date','Global_Mean','North_H_Mean','South_H_Mean',
                   'Tropics_Mean']
    elec_hdrs = ['Date','Electricity Direct Use','Electricity End Use, Total',
                 'Electricity Exports','Electricity Imports',
                 'Electricity Net Generation, Commercial Sector',
                 'Electricity Net Generation, Electric Power Sector',
                 'Electricity Net Generation, Industrial Sector',
                 'Electricity Net Generation, Total',
                 'Electricity Net Imports',
                 'Electricity Retail Sales, Total',
                 'Transmission and Distribution Losses and Unaccounted for']
    rec_hdrs = ['Date','Months_Elapsed_Since_Current_Recession_Began',
                'Months_Elapsed_Since_Last_Recession_Ending']

    cv = {'Date': date_fixer}

    precipitation = pd.read_csv(precipitation_f, names = precip_hdrs, \
                                converters = cv, skiprows = 1)
    electricity = pd.read_csv(electricity_f, names = elec_hdrs, \
                              converters = cv, skiprows = 1)
    recessions = pd.read_csv(recessions_f, names = rec_hdrs, converters = cv,\
                             skiprows = 1)

    dataframes = [precipitation, electricity, recessions]

    return dataframes



def date_fixer(datestring):
    '''
    Fixes dates that come in 'YYYY-MM' format and changes them to datetime.

    Inputs:
        datestring (string): A date in 'YYYY-MM' format.

    Output:
        None.

    Returns:
        date (datetime object): A date as a datetime object.
    '''

    date = dt.strptime(datestring,'%Y-%m')

    return date




def merge_dfs(dataframes_list):
    '''
    '''

    if len(dataframes_list) == 2:
        df_l = dataframes_list[0]
        df_r = dataframes_list[1]
        merged_df = df_l.merge(df_r, how = 'inner', on = 'Date')
        return merged_df

    else:
        df_l = dataframes_list[0]
        return df_l.merge(merge_dfs(dataframes_list[1:]))











dataframes = read_files()


merged_df = merge_dfs(dataframes)
