wbdata.py crawls specified data from world bank's GEM data catalog. 
Right now it only supports specified countries and indicators. 
Will add features to include more options to search in this data catelog. 

Current features:
- get_indicators: tells user which indicators are available for downloading
- get_countries: tells user indicators in which countries are available
- create_df: takes a country, an indicator, start and end date, as well as an output filename. 
             saves data in a csv file. 

Next step: 
- provides country/indicator search feature
- crawl from GEM commodities, which have a slightly different api structure
- page turning during crawling (instead of setting a per_page ceiling)
- add more failure cases
- merge data from different indicators