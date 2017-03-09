import requests
import pandas as pd
import itertools


BASIC_FORMAT = 'http://api.worldbank.org/'

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


def get_commodities():
    '''
    '''
    return set(commodities)


def build_country_code(country):
    '''
    '''
    if country in COUNTRY_CODES:
        country_code = COUNTRY_CODES[country]
    
    else:
        raise ValueError('do not support country: ' + country)

    return 'countries/' + country_code


def build_indicator_code(indicator):
    '''
    '''
    if indicator in INDICATORS:
        indicator_code = INDICATORS[indicator]
    
    else:
        raise ValueError('do not support indicator: ' + indicator)
    
    return '/indicators/' + indicator_code


def build_commodity_indicator_code(commodity):
    '''
    '''
    if commodity in COMMODITIES:
        commodity_code = COMMODITIES[commodity]
    
    else:
        raise ValueError('do not support commodity: ' + commodity)
    
    return 'countries/all/indicators/' + commodity_code


def define_date(yymm=None):
    '''
    Take a tuple of six-digit year and month integers
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
    '''
    date = define_date(yymm)

    if commodities:
        commodity = build_commodity_indicator_code(indicator)
        return BASIC_FORMAT + commodity + '?format=json' + date + '&per_page=5000'
    
    country = build_country_code(country)
    indicator = build_indicator_code(indicator)
    
    api = BASIC_FORMAT + country + indicator + '?format=json' + date + '&per_page=5000' 
    #better make a page-turning algorithm

    return api 


def load_data(country, indicator, yymm=None, commodities=False):
    '''
    '''
    myurl = build_api_link(country, indicator, yymm, commodities)
    r = create_request_object(myurl)
    return r.json()  #check the string r.content

    
def crawl_data(country, indicator, yymm=None, commodities=False):
    '''
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
    Select explanatory variables from world bank's GEM datalog
    '''
    if country_lst is None:
        country_lst = get_countries()
    
    if indicator_lst is None:
        indicator_lst = get_indicators()

    return list(itertools.product(country_lst, indicator_lst))


def create_predictors_df(country_lst=None, indicator_lst=None, yymm=None, \
                         outfile='./worldbank/gem.csv'):
    '''
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
   