import numpy as np
import pandas as pd
import os

PATH = '../scrapers/precipitation_maps/'
OUT_FILE = 'precipitation_means.csv'



def gen_filenames():
    '''
    Generates filenames for the precipitation csv maps downloaded via the
    precipitation scraper.

    Inputs:
        None.

    Outputs:
        None.

    Returns:
        filenames (list of strings): List of the filenames of the csv maps
                                     downloaded via the precipitation scraper.
    '''
    filenames = []

    csv = '.csv'

    years = [x for x in range(1998,2017)]

    for year in years:
        if year != 2016:
            for m in range(1,13):
                if m < 10:
                    month = '0' + str(m)
                else:
                    month = str(m)
                filename = str(year) + '-' + month + csv
                filenames.append(filename)
        else:
            for m in range(1,9):
                month = '0' + str(m)
                filename = str(year) + '-' + month + csv
                filenames.append(filename.strip("b'"))

    return filenames



def read_map(fname):
    '''
    Creates a map dataframe from the data in the file with the given filename.

    Inputs:
        fname (string): The name of the file to be read.

    Outputs:
        None.

    Returns:
        clean_map (pandas dataframe): A csv map read from the file with missing
                                      values replaced with NaN.
    '''

    filename = os.path.join(PATH, fname)
    c = [x for x in range (1,361)]

    map_df = pd.read_csv(filename, names=c)
    clean_map = map_df.replace(99999,np.NaN)

    return clean_map




def calc_means(clean_map):
    '''
    Calculates the mean precipitation in millimeters for the given map.

    Inputs:
        clean_map (pandas dataframe): A csv map with missing values replaced
                                      with NaN.

    Outputs:
        None.

    Returns:
        values (tuple of floats): The global mean, northern-hemisphere mean,
                                  and southern-hemisphere mean for the given
                                  map's precipitation levels.
    '''

    north = clean_map[:90]
    south = clean_map[90:]

    global_mean = clean_map.mean().mean()

    north_mean = north.mean().mean()

    south_mean = south.mean().mean()

    values = global_mean, north_mean, south_mean

    return values





def write_csv(array):
    '''
    Ouputs a csv file with the global, northern, & southern mean precipitation
    levels for each month.

    Note:  There was no data for the month of 2013 January.

    Inputs:
        array (numpy array): An array containing the month id and that month's
                             precipitation means.

    Outputs:
        A file named precipitation_means.csv.

    Returns:
        None.
    '''

    print('\tWriting file:', OUT_FILE)

    csv_file = open(OUT_FILE, 'w')
    headers = 'Date,Global_Mean,North_H_Mean,South_H_Mean\n'
    com = ','

    csv_file.write(headers)

    for line in array:
        filename = line[0]
        date = filename[0:7] + com

        data = line[1]

        csvs = date

        for datum in data[:-1]:
            string = str(datum) + com
            csvs += string

        csvs += str(data[-1]) + '\n'

        csv_file.write(csvs)

    csv_file.close()



def process_maps(filenames):
    '''
    Processes the maps defined in the list of filenames, outputting a file with
    mean precipitation values for each month.

    Inputs:
        filenames (list of strings): A list of filenames.

    Outputs:
        precipitation_means.csv (via write_csv()).

    Returns:
        None.
    '''

    lines_list = []

    for filename in filenames:
        clean_map = read_map(filename)
        values = calc_means(clean_map)
        data_tuple = ((filename,values))
        lines_list.append(data_tuple)

    write_csv(lines_list)




filenames = gen_filenames()

process_maps(filenames)
