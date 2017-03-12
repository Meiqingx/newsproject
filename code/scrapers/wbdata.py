import requests
import pandas as pd
import itertools
import os


DOMAIN_NAME = 'http://api.worldbank.org/'

COUNTRY_CODES = {'United States': 'USA', 'China': 'CHN','Germany':'DEU', 
                 'Japan': 'JPN', 'United Kingdom': 'GBR', 'India': 'IND', 
                 'Brazil': 'BRA', 'World':'WLD'}

INDICATORS = {'stock': 'DSTKMKTXD', 'real exchange rate':'REER', 
              'nomial exchange rate': 'NEER', 'industrial production': 'IPTOTNSKD', 
              'CPI': 'CPTOTNSXN'}

COMMODITIES = {'coffee': 'COFFEE_ROBUS', 'agriculture': 'IAGRICULTURE', 'beverages': 'IBEVERAGES',
                'beef': 'BEEF', 'aluminum': 'ALUMINUM', 'metal': 'IMETMIN', 
                'brent oil': 'CRUDE_BRENT', 'sugar': 'SUGAR_WLD', 'grains': 'IGRAINS', 
                'gold': 'GOLD', 'tabacoo': 'TOBAC_US'}

#########################################
# This module downloads data using      #
# world bank's api structure. It        #
# downloads 40 economic indicators from # 
# GEM (Global  Economi Monitor) data    #
# catalog and 11 commodities from GEM   #
# Commodities data catalog.             #
#########################################

def create_request_object(myurl):
    '''
    Take an url and create a request object. 
    '''
    r = requests.get(url=myurl)
    return r


def get_countries():
    '''
    Return a set of countries supported
    '''
    return set(COUNTRY_CODES)


def get_indicators():
    '''
    Return a set of economic indicators supported
    '''
    return set(INDICATORS)


def get_commodities():
    '''
    Returan a set of commodities supported
    '''
    return set(COMMODITIES)


def build_country_code(country):
    '''
    Build the url path that specifies a country. 
    '''
    if country in COUNTRY_CODES:
        country_code = COUNTRY_CODES[country]
    
    else:
        raise ValueError('do not support country: ' + country)

    return 'countries/' + country_code


def build_indicator_code(indicator):
    '''
    Build the url path that specifies an indicator. 
    '''
    if indicator in INDICATORS:
        indicator_code = INDICATORS[indicator]
    
    else:
        raise ValueError('do not support indicator: ' + indicator)
    
    return '/indicators/' + indicator_code


def build_commodity_indicator_code(commodity):
    '''
    Build the url path that specifies a commodity. 
    '''
    if commodity in COMMODITIES:
        commodity_code = COMMODITIES[commodity]
    
    else:
        raise ValueError('do not support commodity: ' + commodity)
    
    return 'countries/all/indicators/' + commodity_code


def define_date(yymm=None):
    '''
    Take a tuple of six-digit year and month integers, 
    which represents start and end date, and return 
    a proper date query format for world bank api.

    Example input: (198001, 201612)

    If no parameter is passed, it downloads data from 1960-01 to now 2017-03, 
    1960 is the starting record of world bank GEM-Commodities data catalog. 
    '''
    if yymm is None:
        date_code = '1960M01:2017M03'
    
    else:
        start_date, end_date = yymm
        start = str(start_date)
        end = str(end_date)
        date_code = start[0:4] + 'M' + start[4:] + ':' + end[0:4] + 'M' + end[4:]
    
    return '&date=' + date_code
    

def build_api_link(country, indicator, yymm=None, commodities=False):
    '''
    Build the api link to the data of a desired desired indicator. 
    Take a country name, an indicator name, start and end date (optional), 
    and whether the indicator is a commodity or not. Return a link.  
    
    Inputs: 
        country: a country label (example: 'Germany')
        indicator: an indicator label (example: 'coffee')
        yymm: (a tuple of integers )start and end year-month 
              Example: (198001, 201612)
        commodities: by default is False. Commodities are also indicators 
                     in world bank's api structure. But they do not have by country 
                     values, only all countries values. So the logic to build
                     api link is a bit different. 
   
    Returns:
        (str) a complete link

    '''
    date = define_date(yymm)

    if commodities:
        commodity = build_commodity_indicator_code(indicator)
        return DOMAIN_NAME + commodity + '?format=json' + date + '&per_page=5000'
    
    country = build_country_code(country)
    indicator = build_indicator_code(indicator)
    
    api = DOMAIN_NAME + country + indicator + '?format=json' + date + '&per_page=5000' 

    return api 


def load_data(country, indicator, yymm=None, commodities=False):
    '''
    Take a country name, an indicator name, a start-end date pair, and 
    evaluation of the indicator is a commodity or not, build the api link, 
    download and decode JSON data. 
    '''
    myurl = build_api_link(country, indicator, yymm, commodities)
    r = create_request_object(myurl)
    return r.json()

    
def crawl_data(country, indicator, yymm=None, commodities=False):
    '''
    Take a country, an indicator name, a start-end date pair, and evaluation 
    of whether the indicator is a commodity or not, and return pared data. 

    Returns:
        indicator: official name of the indicator in world bank's dataset
        country: which country the data is about
        val: a list of indicator values
        date: a list of date (year-month format) corresponding to 
              the values above

    '''
    content = load_data(country, indicator, yymm, commodities)
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


def select_gem_vars(country_lst=None, indicator_lst=None):
    '''
    Select economic indicators (used as explanatory variables) 
    from world bank's GEM datalog. 

    Inputs:
        If no parameters are passed, it will select a combination of all
        available countries and indicators. 
        (Cartetian product of 8 countries * 5 indicators = 40 variables)
        country_lst: a selected list of countries 
        indicator_lst: a selected list of indicators

    Returns:
        a list of economic indicators (country+indicator) from GEM datacatelog
        Example: [('Japan', 'stock'), ('World', 'industrial production')]

    '''
    if country_lst is None:
        country_lst = get_countries()
    
    if indicator_lst is None:
        indicator_lst = get_indicators()

    return list(itertools.product(country_lst, indicator_lst))


def create_predictors_df(country_lst=None, indicator_lst=None, yymm=None, \
                         outfile='./worldbank/gem.csv'):
    '''
    Create a DataFrame of predictors and save into a csv file. By default download
    all possible predictors supported by this module. 

    Optional inputs:
        a list of countries, a list of indicators, start-end date, and output
        filename. 
    '''
    variables = select_gem_vars(country_lst, indicator_lst)
    
    dfs = [] 

    for var in variables:
        
        country, indicator = var
        
        indicator, country, val, date = crawl_data(country, indicator, yymm)

        col_name = country + ': ' + indicator

        df = pd.DataFrame({col_name: val}, index=date)
        
        dfs.append(df)

    results = pd.concat(dfs, axis=1)
    results.index.name = 'Date'

    results.to_csv(outfile)


def create_commodities_df(commodity_lst=None, yymm=None, \
                         outfile='./worldbank/gem-commodities.csv'):
    '''
    Create a DataFrame of commodities and save into a csv file. This function
    by default downloads all 11 available commodities, spanning all available
    time period from 1960-01 to 2017-03. 
    '''
    if commodity_lst is None:
        commodities_lst = list(COMMODITIES)

    dfs = []

    for commodity in commodities_lst:
        
        indicator, country, val, date = crawl_data(None, commodity, yymm, commodities=True)

        col_name = indicator

        df = pd.DataFrame({col_name: val}, index=date)

        dfs.append(df)

    results = pd.concat(dfs, axis=1)
    results.index.name = 'Date'

    results.to_csv(outfile)

if __name__ == '__main__':

    directory = './worldbank'

    if not os.path.exists(directory):
        os.makedirs(directory)

    create_predictors_df()

    create_commodities_df()
   
