import numpy as np
import pandas as pd
from datetime import datetime as dt



def read_files():
    '''
    '''

    # Filenames
    precipitation_f = '../parsers/precipitation_means.csv'
    electricity_f = '../parsers/electricity_data.csv'
    recessions_f = '../parsers/recessions_data.csv'



    # Column headers for each file
    precip_hdrs = ['Date','Global_Mean_Precipitation',
                   'North_H_Mean_Precipitation','South_H_Mean_Precipitation',
                   'Tropics_Mean_Precipitation']

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





    # The date_fixer function will be used as a converter
    cv = {'Date': date_fixer}

    # Create individual dataframes
    precipitation = pd.read_csv(precipitation_f, names = precip_hdrs, \
                                converters = cv, skiprows = 1)
    electricity = pd.read_csv(electricity_f, names = elec_hdrs, \
                              converters = cv, skiprows = 1)
    recessions = pd.read_csv(recessions_f, names = rec_hdrs, converters = cv,\
                             skiprows = 1)




    # Add dataframes to a list
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

    if len(dataframes_list) < 2:
        return dataframes_list

    elif len(dataframes_list) == 2:
        df_l = dataframes_list[0]
        df_r = dataframes_list[1]
        merged_df = df_l.merge(df_r, how = 'inner', on = 'Date')
        return merged_df

    else:
        df_l = dataframes_list[0]
        return df_l.merge(merge_dfs(dataframes_list[1:]))




def gen_sqrs_cbcs(df):
    '''
    Generates squared and cubic terms for all variables in the data frame.

    Inputs:
        df (pandas dataframe): The dataframe in question.

    Outputs:
        None

    Returns:
        None
    '''

    names = list(df.columns)[1:]

    sqr_names = [x + ' ** 2' for x in names]
    cbc_names = [x + ' ** 3' for x in names]

    for i, name in enumerate(names):
        df[sqr_names[i]] = df[name].map(lambda x: x ** 2)
        df[cbc_names[i]] = df[name].map(lambda x: x ** 3)




dataframes = read_files()


merged_df = merge_dfs(dataframes)

gen_sqrs_cbcs(merged_df)
