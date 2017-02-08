import os
import re
import bs4
import requests

OUTPUT_DIR = 'recessions_data'
OUTPUT_START = 'recession_start_dates'
OUTPUT_END = 'recession_end_dates'
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
    '''

    rqst = requests.get(url)

    markup = rqst.text.encode('iso-8859-1')

    soup = bs4.BeautifulSoup(markup, 'html5lib')

    return soup


def process_page(soup):
    '''
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
    return start_dates, end_dates


def clean_dates(dates):
    '''
    '''

    clean_dates = []

    for date in dates:
        clean_date = re.findall('[A-Z][a-z]*[\s]+[1-2][0-9][0-9][0-9]', date)
        clean_dates.append(clean_date)

    return clean_dates




create_output_dir()

soup = get_page(URL)

start_dates, end_dates = process_page(soup)

#start_dates = clean_dates(start_dates)

#end_dates = clean_dates(end_dates)
