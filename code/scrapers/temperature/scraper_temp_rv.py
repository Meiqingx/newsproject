# CS122
# Gruop Project

from bs4 import BeautifulSoup
import requests
import html2text
import re
import numpy as np
import pandas as pd



initial_url = "https://data.giss.nasa.gov/gistemp/"

def get_url_list(initial_url):
    '''
    Gets the list of urls to scrape from the web page

    Input: url

    Output: list of urls
    '''
    rqst = requests.get(initial_url)
    markup = rqst.text.encode('iso-8859-1')
    soup = BeautifulSoup(markup, 'lxml')
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
    for extract_url in urls_list: 
        testing_url = base_url + extract_url
        file_name = extract_url[13:-4] + ".txt"
        page = urllib.request.urlopen(testing_url)
        html_content = page.read()
        text = html_content.decode('utf-8')
        w = open(file_name, 'w')
        w.write(text)
        w.close()
        print("File", file_name, "ready to use")

    return print("FINISH")


def generate_df(file):
    '''
    It generates a pandas dataframe from the name of a file

    Input:
        file: name of the file
    Output:
        pandas dataframe
    '''
    num_lines = sum(1 for line in open(file))

    # Skiprows generator
    num_cycles = ((num_lines - 14) // 20) - 1
    low_bound = 29
    upper_bound = 30

    skip_list = []
    for i in range(num_cycles):
        skip_list.append(low_bound + 22*i)
        skip_list.append(upper_bound + 22*i)

    data = pd.read_csv(file, header = 5, delimiter=r"\s+",  
        skipfooter = 7, skip_blank_lines = True, engine = 'python',
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



