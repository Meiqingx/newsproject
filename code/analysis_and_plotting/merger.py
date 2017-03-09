import numpy as np
import pandas as pd
from datetime import datetime as dt
import csv


def read_files():
    '''
    '''

    # Filenames
    precipitation_f = '../parsers/precipitation_means.csv'
    electricity_f = '../parsers/electricity_data.csv'
    recessions_f = '../parsers/recessions_data.csv'
    worldbank_f = '../scrapers/worldbank/gem.csv'
    commodities_f = '../scrapers/worldbank/gem-commodities.csv'


    # Column headers for each file
    precip_hdrs = ['Date','Global Monthly Mean Precipitation',
                   'Northern Hemisphere Monthly Mean Precipitation',
                   'Southern Hemisphere Monthly Mean Precipitation',
                   'Tropics Monthly Mean Precipitation']

    elec_hdrs = ['Date','Electricity Direct Use','Electricity End Use, Total',
                 'Electricity Exports','Electricity Imports',
                 'Electricity Net Generation, Commercial Sector',
                 'Electricity Net Generation, Electric Power Sector',
                 'Electricity Net Generation, Industrial Sector',
                 'Electricity Net Generation, Total',
                 'Electricity Net Imports',
                 'Electricity Retail Sales, Total',
                 'Transmission and Distribution Losses and Unaccounted for']

    rec_hdrs = ['Date','Months Elapsed Since Current Recession Began',
                'Months Elapsed Since Last Recession Ending']


    # The date_fixer function will be used as a converter
    cv = {'Date': date_fixer}

    # Create individual dataframes
    precipitation = pd.read_csv(precipitation_f, names = precip_hdrs, \
                                converters = cv, skiprows = 1)
    precipitation = precipitation.interpolate()

    electricity = pd.read_csv(electricity_f, names = elec_hdrs, \
                              converters = cv, skiprows = 1)
    recessions = pd.read_csv(recessions_f, names = rec_hdrs, converters = cv,\
                             skiprows = 1)

    #meiqing: I set descriptive headers in my crawler, so did not put a new set of labels here
    worldbank_gem = pd.read_csv(worldbank_f, converters=cv)

    commodities = pd.read_csv(commodities_f, converters=cv)

    oil = commodities[['Date', 'Crude oil, Brendt, $/bbl, nominal$']].copy()
    commodities = commodities.drop('Crude oil, Brendt, $/bbl, nominal$', axis=1)

    predictor_dfs = [precipitation, electricity, recessions, worldbank_gem, oil]
    outcomes = commodities

    return predictor_dfs, outcomes



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



def write_csv(df,filename):
    '''
    Writes a dataframe to a csv file.

    Inputs:
        df (pandas dataframe): The final dataframe to be written.

    Outputs:
        A csv file with the name of OUT_FILE.

    Returns:
        None.
    '''
    dt = 'Date'
    dt_fmt = '%Y-%m'

    df.to_csv(path_or_buf = filename, header=True, index=False,\
                     date_format = dt_fmt)


predictor_dfs, outcomes = read_files()

predictors = merge_dfs(predictor_dfs)

gen_sqrs_cbcs(predictors)

write_csv(predictors,'predictors.csv')
write_csv(outcomes,'outcomes.csv')
