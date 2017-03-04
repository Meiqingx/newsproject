import requests
import pandas as pd
import itertools


BASIC_FORMAT = 'http://api.worldbank.org/'

COUNTRY_CODES = {'United States': 'USA', 'China': 'CHN','Germany':'DEU', 
                 'Japan': 'JPN', 'United Kingdom': 'GBR', 'India': 'IND', 
                 'Brazil': 'BRA', 'World':'WLD'}

INDICATORS = {'stock': 'DSTKMKTXD', 'real exchange rate':'REER', 
              'nomial exchange rate': 'NEER', 'industrial production': 'IPTOTNSKD', 
              'CPI': 'CPTOTSAXMZGY', }

# create a country lookup function/class..

def create_request_object(myurl):
    '''
    '''
    r = requests.get(url=myurl)
    return r


def get_countries():
    '''
    '''
    return set(COUNTRY_CODES)


def get_indicators():
    '''
    '''
    return set(INDICATORS)


def build_country_code(country):
    '''
    '''
    if country in COUNTRY_CODES:
        country_code = COUNTRY_CODES[country]
    
    else:
        raise ValueError('invalid country')

    return 'countries/' + country_code


def build_indicator_code(indicator):
    '''
    '''
    if indicator in INDICATORS:
        indicator_code = INDICATORS[indicator]
    else:
        raise ValueError('invalid indicator')
    return '/indicators/' + indicator_code


def define_date(yymm=None):
    '''
    Take a tuple of six-digit year and month integers
    '''
    if yymm is None:
        date_code = '1950M01:2017M03'
    else:
        start_date, end_date = yymm
        start = str(start_date)
        end = str(end_date)
        date_code = start[0:4] + 'M' + start[4:] + ':' + end[0:4] + 'M' + end[4:]
    return '&date=' + date_code
    

def build_api_link(country, indicator, yymm=None):
    '''
    '''
    country = build_country_code(country)
    indicator = build_indicator_code(indicator)
    date = define_date(yymm)

    api = BASIC_FORMAT + country + indicator + '?format=json' + date + '&per_page=1000' 
    #better make a page-turning algorithm

    return api


def load_data(country, indicator, yymm=None):
    '''
    '''
    myurl = build_api_link(country, indicator, yymm)
    r = create_request_object(myurl)
    return r.json()  #check the string r.content

    
def crawl_data(country, indicator, yymm=None):
    '''
    '''
    content = load_data(country, indicator, yymm)
    data = content[1]
    
    indicator = data[0]['indicator']['value'].rstrip(',')
    country = data[0]['country']['value']
    val = []
    date = []
    
    for datum in data:
        val.append(datum['value'])
        ym = datum['date'][:4] + '-' + datum['date'][5:]
        date.append(ym)
    
    return indicator, country, val, date


def select_vars(country_lst=None, indicator_lst=None):
    '''
    Select variables 
    '''
    if country_lst is None:
        country_lst = get_countries()
    
    if indicator_lst is None:
        indicator_lst = get_indicators()

    return list(itertools.product(country_lst, indicator_lst))


def create_df(country_lst=None, indicator_lst=None, yymm=None, outfile='./worldbank/gem.csv'):
    '''
    '''
    variables = select_vars(country_lst, indicator_lst)
    dfs = [] 

    for var in variables:
        
        country, indicator = var
        
        indicator, country, val, date = crawl_data(country, indicator, yymm)

        col_name = country + ': ' + indicator

        df = pd.DataFrame({col_name: val},
                           index=date)
        
        dfs.append(df)

    results = pd.concat(dfs, axis=1)
    results.index.name = 'Date'

    results.to_csv(outfile)

