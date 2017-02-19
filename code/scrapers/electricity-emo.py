import os
import numpy as np
import pandas as pd
from datetime import datetime as dt


URL = 'http://www.eia.gov/totalenergy/data/browser/xls.cfm?tbl=T07.01'

OUTPUT_DIR = 'electricity_data'
OUTPUT_FILE = 'electricity_data.csv'

'''
create_output_dir()

filename = '../parsers/electricity_file/MER_T07_01.csv'


'''

#file_dl = urllib.request.urlopen(URL)
#file_csv = csv.reader(file_dl)





#rqst = requests.get(URL)
#csv = rqst.text.encode('iso-8859-1')


'''
decoded_content = download.content.decode('utf-8')

    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    my_list = list(cr)
    for row in my_list:
        print(row)

'''



#df = pd.read_csv(URL)
