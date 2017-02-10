import os
import re
import bs4
import requests
import numpy as np

OUTPUT_DIR = 'recessions_data'
OUTPUT_FILE = 'recession_dates.csv'
URL = 'http://www.nber.org/cycles.html'

def create_output_dir():
    '''
    Creates directory if recessions_data directory does not already exist.

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


def get_page(url):
    '''
    Downloads the page at the given URL and creates a BeautifulSoup object.

    Inputs:
        url (string): The URL to be accessed.

    Outputs:
        None.

    Returns:
        soup (BeautifulSoup object): The BeautifulSoup made from the URL.
    '''

    rqst = requests.get(url)

    markup = rqst.text.encode('iso-8859-1')

    soup = bs4.BeautifulSoup(markup, 'html5lib')

    return soup


def process_page(soup):
    '''
    Processes a BeautifulSoup object and returns lists of the recession start
    and end dates.

    Inputs:
        soup (BeautifulSoup object): The BeautifulSoup object to be processed.

    Outputs:
        None.

    Returns:
        clean_start (list of strings): A list of YYYY-MM recession start dates.
        clean_end (list of strings): A list of YYYY-MM recession end dates.
    '''

    block = soup.find_all('div', align = "center")

    start_dates = []
    end_dates = []

    for idx, item in enumerate(block):
        lines = str(item).split('br/')
        for line in lines[11:44]:
            start_dates.append(line)
        for line in lines[44:78]:
            end_dates.append(line)

    clean_start = clean_dates(start_dates)
    clean_start.insert(0,[''])

    clean_end = clean_dates(end_dates)

    return clean_start, clean_end


def clean_dates(dates):
    '''
    Takes in a list of dates in 'Month YYYY' format and switches them to
    YYYY-MM format.

    Inputs:
        dates (list of strings): The list of dates to be cleaned.

    Outputs:
        None.

    Returns:
        clean_dates (list of strings): The cleaned list of dates in YYYY-MM
                                       format.
    '''

    expr = '[A-Z][a-z]*[\s]+[1-2][0-9][0-9][0-9]'

    clean_dates = []

    for date in dates:
        date_string = re.findall(expr, date)[0]
        month, year = date_string.split()
        clean_date = year + ' ' + month
        clean_dates.append([clean_date])

    return clean_dates



def build_array(clean_start, clean_end):
    '''
    Takes lists of cleaned start and end dates and makes an array of them.

    Inputs:
        clean_start (list of strings): A list of the cleaned start dates.
        clean_end (list of strings): A list of the cleaned end dates.

    Outputs:
        None.

    Returns:
        array (numpy array): An array of corresponding start and end dates.
    '''
    start = np.array(clean_start)
    end = np.array(clean_end)

    array = np.hstack((start, end))

    return array



def write_csv(array):
    '''
    Writes a csv file from the given array.

    Inputs:
        array (numpy array): The array to be written.

    Outputs:
        A csv file named OUTPUT_FILE and in OUTPUT_DIR.

    Returns:
        None.
    '''

    headers = 'Start_Date,End_Date\n'

    path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

    csv_file = open(path, 'w')

    csv_file.write(headers)

    for line in array[:-1]:
        start = line[0]
        end = line[1]
        string = start + ',' + end + '\n'
        csv_file.write(string)

    start = array[-1][0]
    end = array[-1][1]

    string = start + ',' + end

    csv_file.write(string)

    csv_file.close()



create_output_dir()

soup = get_page(URL)

clean_start, clean_end = process_page(soup)

array = build_array(clean_start, clean_end)

write_csv(array)
