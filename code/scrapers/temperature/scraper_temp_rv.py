# CS122
# Group Project

from bs4 import BeautifulSoup
import requests
import os
import html2text
import lxml
import re
from urllib.request import urlopen
import numpy as np
import pandas as pd


def make_output_dir():
    '''
    Create directory of output data if it does not already exist
    '''
    cur_path = os.path.split(os.path.abspath(__file__))[0]
    output_fldr = 'data'
    output_dir = os.path.join(cur_path, output_fldr)
    if not os.access(output_dir, os.F_OK):
        os.makedirs(output_dir)

    return(output_dir)


def get_url_list(initial_url):
    '''
    Gets the list of urls to scrape from the web page

    Input: url

    Output: list of urls
    '''
    rqst = requests.get(initial_url)
    markup = rqst.text.encode('iso-8859-1')
    soup = BeautifulSoup(markup, 'html.parser')
    links = soup.find_all("a")

    aux_list = []
    for a in links:
        if a.get("href") == None:
            pass
        else: 
            url_converted = a.get("href")
            aux_list.append(url_converted)

    urls_list = []
    for possible_link in aux_list:
        if ".txt" in possible_link and "tabledata" in possible_link:
            urls_list.append(possible_link)

    return urls_list


def save_plain_text(urls_list, base_url = "https://data.giss.nasa.gov/gistemp/"):
    '''
    Save the extracted plain text to txt files

    Inputs:
        urls_list: list with urls
        base_url: main url form the original domain

    Output: None; it saves the files
    '''
    list_name_files = []
    for extract_url in urls_list: 
        testing_url = base_url + extract_url
        file_name = extract_url[13:-4] + ".txt"
        page = urlopen(testing_url)
        html_content = page.read()
        text = html_content.decode('utf-8')
        w = open(file_name, 'w')
        w.write(text)
        w.close()
        print("File", file_name, "ready to use")
        list_name_files.append(file_name)

    print("FINISH")

    return list_name_files

# Save plain text
# save_plain_text(urls_list)

def generate_df(file):
    '''
    It generates a pandas dataframe from the name of a file

    Input:
        file: name of the file
    Output:
        pandas dataframe
    '''
    num_lines = sum(1 for line in open(file))
    num_cycles = ((num_lines - 14) // 20) - 1

    # Skiprows generator
    if 'Annual mean' in open(file).read():
        low_bound = 31
        upper_bound = 32

        skip_list = []
        for i in range(num_cycles):
            skip_list.append(low_bound + 22*i)
            skip_list.append(upper_bound + 22*i)
            skip_list.append(low_bound + 23*i)
            skip_list.append(upper_bound + 23*i)

        data = pd.read_csv(file, header = 7, delimiter=r"\s+",  
            skipfooter = 2, skip_blank_lines = True, engine = 'python',
            skiprows = skip_list, 
            usecols = list(range(13)))
    else:
        low_bound = 29
        upper_bound = 30

        skip_list = []
        for i in range(num_cycles):
            skip_list.append(low_bound + 22*i)
            skip_list.append(upper_bound + 22*i)

        data = pd.read_csv(file, header = 5, delimiter=r"\s+",  
            skipfooter = 8, skip_blank_lines = True, engine = 'python',
            skiprows = skip_list, 
            usecols = list(range(13)))

    return data


def print_full(x):
    '''
    Allow to print a complete pandas dataframe

    Input:
        dataframe
    '''
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')


# Run the file
output_dir = make_output_dir()   
initial_url = "https://data.giss.nasa.gov/gistemp/"
urls_list = get_url_list(initial_url)
#  names_files = save_plain_text(urls_list)

names_files = ['GLB.Ts+dSST.txt',
 'NH.Ts+dSST.txt',
 'SH.Ts+dSST.txt',
 'ZonAnn.Ts+dSST.txt',
 'GLB.Ts.txt',
 'NH.Ts.txt',
 'SH.Ts.txt',
 'ZonAnn.Ts.txt']

# Create data frames
new_names = []
for i, name in enumerate(names_files):
    if "Zon" not in name:
        new_names.append(name[:7])
        globals()['data_%s' % name[:7]] = generate_df(names_files[i])

# Need to merge and save dataframes

######################
# COMPATIBILITY NEEDED
######################

# Set index

def compatibility(df):
    df = df.set_index(df['Year'])
    df = df.drop(['Year'], axis=1)
    df = df.stack()
    df.index = pd.PeriodIndex(start = '1880-01', freq='M', periods = len(df))

    return df



