wbdata.py crawls specified data from world bank's GEM and GEM Commodities data catalogs. 

Right now it only supports specified countries and indicators. 


Current features:
- get_indicators: tells user which indicators are available for downloading

- get_countries: tells user indicators in which countries are available

- get_commodities: tells user what commodities are used as dependent variables (except cruid oil)

- create_predictors_df: if no parameters are passed, the default is to create a dataframe 
                        including all indicators from all available countries and save it into a predefined filename. 
                        optional parameters include list of countries, list of indicators, start and end date, as well as an output filename.  

- create_commodities_df: if no parameters are passed, the default is to create a dataframe
                         including all commodities


Optional optimization plans: 
- provides country/indicator search feature
- page turning during crawling (instead of setting a per_page ceiling)
- add more failure cases
