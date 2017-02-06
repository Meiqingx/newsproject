import numpy as np
#import os

def gen_filenames():
    '''
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
                filenames.append(filename)

    return filenames
