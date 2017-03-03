import numpy as np
import pandas as pd
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta as rd

#import os

IN_FILE = '../scrapers/recessions_data/recession_dates.csv'
OUT_FILE = 'recessions_data.csv'

def read_file(fname):
    '''
    Reads in the recession_dates.csv file, converts the dates, replaces missing
    values with np.NaN, and returns the cleaned dataframe.

    Inputs:
        fname (string): The name of the file to be read.

    Outputs:
        None.

    Returns:
        clean_recessions (pandas dataframe): The cleaned dataframe.
    '''

    date_conv = {'Start_Date': date_fixer, 'End_Date': date_fixer}

    recessions = pd.read_csv(fname,converters=date_conv)
    clean_recessions = recessions.replace('',np.NaN)

    return clean_recessions



def date_fixer(datestring):
    '''
    Fixes a datestring by making it a datetime object.

    Input:
    datestring (string): A date in 'YYYY Month' format.

    Output:
        None.

    Returns:
        date (datetime): A corrected date (or np.NaN if datestring was '').
    '''

    if datestring == '':
        return np.NAN

    else:
        date = dt.strptime(datestring,'%Y %B')

        return date



def build_df(clean_recessions):
    '''
    Takes in a cleaned recessions dataframe and builds the output dataframe.

    Inputs:
        clean_recessions (pandas dataframe): The cleaned recessions dataframe.

    Outputs:
        None.

    Returns:
        df (pandas dataframe): A dataframe of YYYY-MM dates ranging from the
                               beginning of the recessions dataset to the
                               present with columns for months elapsed since
                               the most recent recession began and months
                               elapsed since the last recession ending.
    '''

    months_list = gen_months_list(clean_recessions)

    dms = 'Months Elapsed Since Current Recession Began'
    dme = 'Months Elapsed Since Last Recession Ending'

    rec_start_deltas, rec_end_deltas = gen_deltas(clean_recessions, months_list)

    df_dicto = {dms: rec_start_deltas, dme: rec_end_deltas}
    #df_dicto = {ym: months_list, dms: rec_start_deltas, dme: rec_end_deltas}

    df = pd.DataFrame(df_dicto, index = months_list)
    #df = []

    return df



def dy2dm(reldel):
    '''
    Takes a relative delta object and converts it to delta-months.

    Inputs:
    reldel (relative delta object):  The difference between two dates.

    Outputs:
        None.

    Returns:
        dm (int): Delta-months, the difference between two dates in months.
    '''
    m = reldel.months
    y = reldel.years
    dm  = int(y * 12 + m)

    return dm



def gen_months_list(clean_recessions):
    '''
    Generates the list of YYYY-MMs ranging from the start of the first economic
    recession listed in the data to the present month.

    Inputs:
        clean_recessions (pandas dataframe): The cleaned recessions dataframe.

    Outputs:
        None.

    Returns:
        months_list (list of datetime objects): List of all the months ranging
                                                from the first start date in
                                                the recession data to the
                                                present month.
    '''

    dates = get_dates(clean_recessions)
    current_date, first_start_date, first_end_date = dates

    first_start_year = first_start_date.year
    first_start_month = first_start_date.month

    current_year = current_date.year
    current_month = current_date.month

    years = [x for x in range(first_start_year, current_year + 1)]
    months = [x for x in range(1,13)]

    months_list = []

    for year in years[:-1]:
        for month in months:
            datestring = str(year) + ' ' + str(month)
            date = dt.strptime(datestring, '%Y %m')
            months_list.append(date)

    for month in range(1,current_month + 1):
        datestring = str(current_year) + ' ' + str(month)
        date = dt.strptime(datestring, '%Y %m')
        months_list.append(date)

    return months_list



def gen_deltas(clean_recessions, months_list):
    '''
    For each month in months_list, generates the months elapsed since the start
    of the most recent recession and the most recent recession ending.

    Inputs:
        clean_recessions (pandas dataframe):  The cleaned recessions dataframe.
        months_list (list of datetime objects): List of the months ranging from
                                                the start of the earliest
                                                recession in the data and the
                                                current month.

    Outputs:
        None.

    Returns:
        rec_start_deltas (list of ints): List of the number of months elapsed
                                         since the start of the most recent
                                         recession, corresponding to the dates
                                         in months_list.
        rec_end_deltas (list of ints): List of the number of months elapsed
                                       since the most recent recession ending,
                                       corresponding to the dates in
                                       months_list.
    '''

    dates = get_dates(clean_recessions)
    current_date, first_start_date, first_end_date = dates

    end_delta = dy2dm(rd(first_start_date, first_end_date)) + 1

    rec_start_deltas = [1]

    rec_end_deltas = [end_delta]

    start_count = 2
    end_count = 1

    start_col = clean_recessions['Start_Date'][2:]
    end_col = clean_recessions['End_Date'][1:]

    for month in months_list[1:]:
        elapsed_start = rec_start_deltas[-1]
        elapsed_end = rec_end_deltas[-1]

        if start_count < len(clean_recessions):
            if month == start_col[start_count]:
                rec_start_deltas.append(1)
                start_count += 1
            else:
                incr = elapsed_start + 1
                rec_start_deltas.append(incr)
        else:
            incr = elapsed_start + 1
            rec_start_deltas.append(incr)

        if end_count < len(clean_recessions):
            if month == end_col[end_count]:
                rec_end_deltas.append(1)
                end_count += 1
            else:
                incr = elapsed_end + 1
                rec_end_deltas.append(incr)
        else:
            incr = elapsed_end + 1
            rec_end_deltas.append(incr)

    return rec_start_deltas, rec_end_deltas



def get_dates(clean_recessions):
    '''
    Returns the current date, the start date of the earliest recession, and the
    end date of the earliest recession, all as datetime objects.

    Inputs:
        clean_recessions (pandas dataframe): The cleaned recessions dataframe.

    Outputs:
        None.

    Returns:
        dates (list of datetime objects): A list of the current date, first
                                          recession start date, and first
                                          recession end date, all as datetime
                                          objects.
    '''
    current_date = dt.strptime('2017 February', '%Y %B')
    first_start_date = clean_recessions['Start_Date'][1]
    first_end_date = clean_recessions['End_Date'][0]

    dates = [current_date, first_start_date, first_end_date]

    return dates



def write_csv(df):
    '''
    Writes a dataframe to a csv file.

    Inputs:
        df (pandas dataframe): The final dataframe to be written.

    Outputs:
        A csv file with the name of OUT_FILE.

    Returns:
        None.
    '''
    ym = 'Year_Month'
    dt_fmt = '%Y-%m'

    df.to_csv(path_or_buf = OUT_FILE, index_label = ym, \
                     date_format = dt_fmt)




clean_recessions = read_file(IN_FILE)

df = build_df(clean_recessions)

write_csv(df)
