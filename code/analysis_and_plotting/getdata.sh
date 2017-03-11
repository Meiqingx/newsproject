#!/bin/bash

cd ../scrapers

echo -e '\nRunning precipitation scraper\n'
python3 precipitation-emo.py

echo -e '\nRunning recessions scraper\n'
python3 recessions-emo.py

echo -e '\nRunning World Bank scraper\n'
python3 wbdata.py



cd temperature

echo -e '\nRunning temperature scraper\n'
python3 scraper_temp_rv.py

echo -e '\nDone scraping all data (except for electricity data,'
echo -e 'which was downloaded by hand)\n\n'




cd ../../parsers

echo -e '\nParsing electricity data\n'
python3 electricity-emo.py

echo -e '\nParsing precipitation data\n'
python3 precipitation-emo.py

echo -e '\nParsing recessions data\n'
python3 recessions-emo.py

echo -e '\nDone parsing all data\n\n'




cd ../analysis_and_plotting

echo -e '\nMerging data\n'
python3 merger.py
echo -e '\nDone merging\n\n'

echo -e '\nBuilding diagnostic plots\n'
python3 graph_builder.py
echo -e '\nDone building diagnostic plots\n\n'

echo -e '\nDone processing data files.  Next step is to analyze and predict.\n\n'
