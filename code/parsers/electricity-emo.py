import numpy as np
import pandas as pd
from datetime import datetime as dt

#URL = 'http://www.eia.gov/totalenergy/data/browser/xls.cfm?tbl=T07.01'

OUTPUT_FILE = 'electricity_data.csv'

def create_output_dir():
    '''
    Creates directory if electricity_data directory does not already exist.

    Inputs:
        None.

    Outputs:
        The output directory at current_path/OUTPUT_DIR.

    Returns:
        None.
    '''

    cur_path = os.path.split(os.path.abspath(__file__))[0]
    output_path = os.path.join(cur_path, OUTPUT_DIR)
    if not os.access(output_path, os.F_OK):
        os.makedirs(output_path)
        print('Creating output directory:', output_path)



def date_fixer(date_int):
    '''
    Fixes dates that come in int(YYYYMM) format and changes them to datetime.

    Inputs:
        date_int (int): A date in YYYYMM format.

    Output:
        None.

    Returns:
        date (datetime object): A corrected date as a datetime object (or
                                np.NaN if the date was invalid).
    '''
    datestring = str(date_int)[0:7]

    if datestring[4:6] == '13':
        return np.NaN

    else:
        date = dt.strptime(datestring,'%Y%m')
        return date



def build_df(filename):
    '''
    Builds a dataframe from the given filename with one row per month and one
    column for each variable.

    Inputs:
        filename (string): The name of the file to be read.

    Outputs:
        None.

    Returns:
        df (pandas dataframe): The final dataframe.
    '''

    c = ['MSN','Date','Billion_Kwatt_Hrs','Column_Order','Description','Unit']
    cv = {'Date': date_fixer}
    uc = ['Date','Billion_Kwatt_Hrs','Description']

    df = pd.read_csv(filename, names = c, converters = cv, skiprows = 1,\
                     usecols = uc).dropna()

    df = df.pivot(index = uc[0], values = uc[1], columns = uc[2])
    df = df.replace('Not Available',np.NaN)

    return df



def write_csv(df):
    '''
    Writes a csv file from the dataframe.

    Inputs:
        df (pandas dataframe): The dataframe to be written.

    Outputs:
        A csv named OUTPUT_FILE.

    Returns:
        None.
    '''

    dt_fmt = '%Y-%m'

    df.to_csv(path_or_buf = OUTPUT_FILE, index_label = 'Date', \
              date_format = dt_fmt)



filename = 'electricity_file/MER_T07_01.csv'

df = build_df(filename)

write_csv(df)
