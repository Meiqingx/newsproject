import numpy as np
import pandas as pd
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta as rd

#import os

IN_FILE = '../scrapers/recessions_data/recession_dates.csv'
OUT_FILE = 'recessions_data.csv'

def read_file(fname):
    '''
    '''

    date_conv = {'Start_Date': date_fixer, 'End_Date': date_fixer}

    recessions = pd.read_csv(fname,converters=date_conv)
    clean_recessions = recessions.replace('',np.NaN)

    return clean_recessions



def date_fixer(datestring):
    '''

    Input:  (string) datestring: A date in 'YYYY Month' format.

    Output: (datetime) date: a corrected date
    '''

    if datestring == '':
        return np.NAN

    else:
        date = dt.strptime(datestring,'%Y %B')

        return date



def build_df(clean_recessions):
    '''
    '''

    months_list = gen_months_list(clean_recessions)

    dms = 'Months_Elapsed_Since_Current_Recession_Began'
    dme = 'Months_Elapsed_Since_Last_Recession_Ending'

    rec_start_deltas, rec_end_deltas = gen_deltas(clean_recessions, months_list)

    df_dicto = {dms: rec_start_deltas, dme: rec_end_deltas}
    #df_dicto = {ym: months_list, dms: rec_start_deltas, dme: rec_end_deltas}

    df = pd.DataFrame(df_dicto, index = months_list)
    #df = []

    return df



def dy2dm(reldel):
    '''
    Takes a relative delta object and converts it to delta-months.

    Input: (relative delta object) reldel:  the difference between two dates

    Output: (int) dm: delta-months, the difference between two dates in months
    '''
    m = reldel.months
    y = reldel.years
    dm  = int(y * 12 + m)

    return dm



def gen_months_list(clean_recessions):
    '''
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

        if start_count < len(clean_recessions) - 2:
            if month == start_col[start_count]:# + 2]:
                rec_start_deltas.append(1)
                start_count += 1
            else:
                incr = elapsed_start + 1
                rec_start_deltas.append(incr)
        else:
            incr = elapsed_start + 1
            rec_start_deltas.append(incr)

        if end_count < len(clean_recessions) - 1:
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
    '''
    current_date = dt.strptime('2017 February', '%Y %B')
    first_start_date = clean_recessions['Start_Date'][1]
    first_end_date = clean_recessions['End_Date'][0]

    dates = [current_date, first_start_date, first_end_date]

    return dates



def write_csv(df):
    '''
    '''
    ym = 'Year_Month'
    dt_fmt = '%Y-%m'

    df.to_csv(path_or_buf = OUT_FILE, index_label = ym, \
                     date_format = dt_fmt)




clean_recessions = read_file(IN_FILE)

df = build_df(clean_recessions)

write_csv(df)
