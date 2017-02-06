import os
import bs4
import queue
import requests

OUTPUT_DIR = 'precipitation_maps'

def create_output_dir():
    '''
    Creates directory if precipitation_maps directory does not already exist.

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



def get_csvs(queue):
    '''
    Downloads csv maps of global precipitation.

    Inputs:
        queue (queue): A queue object containing the URLS of the files to be
                       downloaded.
    Outputs:
        A csv file for every downloaded precipitation map.

    Returns:
        None.
    '''

    path = 'http://neo.sci.gsfc.nasa.gov/servlet/RenderData?si='
    fmt = '&cs=rgb&format=CSV&width=360&height=180'

    for idx in range(queue.qsize()):
        data_tuple = queue.get()
        date, data_id = data_tuple

        url = path + data_id + fmt
        rqst = requests.get(url)
        csv_map = rqst.text.encode('iso-8859-1')

        filename = str(date) + '.csv'
        output_path = os.path.join(OUTPUT_DIR, filename)

        write_csv(csv_map, output_path)

    print('\n\nDone saving files')



def write_csv(csv_map, filename):
    '''
    Takes a csv_map and outputs a csv file.

    Inputs:
        csv_map (csv_map_object):  The data to be written
        filename (str):  The name of the file to be written

    Outputs:
        A csv map with the name [filename].

    Returns:
        None
    '''

    print('\tWriting file:', filename)

    csv_file = open(filename, 'w')

    text_string = str(csv_map)

    text = text_string.strip("b'")

    lines = text.split('\\n')

    for line in lines:
        line += '\n'
        csv_file.write(line)

    csv_file.close()



def create_main_url_list():
    '''
    Creates a list of main-page URLs to be scraped.

    Inputs:
        None.

    Outputs:
        None.

    Returns:
        url_list [list of (year, url) tuples]: A list of tuples with the format
                                               (year, url-for-that-year).
    '''

    print('Creating list of main URLs.')

    url_base = 'http://neo.sci.gsfc.nasa.gov/view.php?datasetId=TRMM_3B43M&year='
    year_range = [x for x in range(1998,2017)]

    url_list = []

    for year in year_range:
        url_year = url_base + str(year)
        url_list.append((year, url_year))

    return url_list



def build_queue(url_list):
    '''
    Builds a queue of the IDs of files to be downloaded.

    Inputs:
        url_list [list of (year, url) tuples]: A list of tuples with the format
                                               (year, url-for-that-year).

    Outputs:
        None.

    Returns:
        q (queue): A queue object containing a (month, month_id) tuple for each
                   file to be downloaded.
    '''

    print('Building queue of files to download.')

    q = queue.Queue()

    for url_tuple in url_list:
        year, url = url_tuple
        months_list = build_months(year)
        q = crawl_page(url, months_list, q)

    return q




def build_months(year):
    '''
    Builds a list of the months of the given year for which data will be
    downloaded.

    Inputs:
        year (int): The given year.

    Outputs:
        None.

    Returns:
        months_list (list of strings): List of months of the given year for
                                       which data will be downloaded.
    '''

    print('Building months list for {}.'.format(year))

    if year == 2016:
        months = [x for x in range(1, 9)]

    else:
        months = [x for x in range(1, 13)]

    months_list = []

    for month in months:
        if month < 10:
            month = '0' + str(month)
        else:
            month = str(month)

        ymd = str(year) + '-' + month
        months_list.append(ymd)

    return months_list




def crawl_page(url, months_list, queue):
    '''
    Crawls the page at url and adds that year's file IDs to the queue.

    Inputs:
        url (string): The URL to be visited.
        months_list (list of strings): A list of the months for which file IDs
                                       must be acquired from the given page.
        queue (queue): A queue containing the current list of file IDs and
                       corresponding dates.
    Outputs:
        None.

    Returns:
        queue (queue): The updated queue.
    '''

    print('Crawling page:', url)

    rqst = requests.get(url)

    markup = rqst.text.encode('iso-8859-1')

    soup = bs4.BeautifulSoup(markup, 'html5lib')

    block = soup.find_all('div', class_='slider-elem month')

    for idx, item in enumerate(block):
        text = str(item)
        text_list = [x for x in text.split()]
        sub_list = text_list[5]
        month_id = sub_list[22:29]
        month = months_list[idx]
        data_tuple = ((month,month_id))
        queue.put(data_tuple)

    return queue



create_output_dir()

main_url_list = create_main_url_list()

queue = build_queue(main_url_list)

get_csvs(queue)
