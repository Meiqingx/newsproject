#!/bin/bash

cd ../scrapers

#python3 precipitation-emo.py
python3 recessions-emo.py
python3 wbdata.py

cd commodities_data

python3 commodities_prices.csv


cd ../temperature

python3 scraper_temp_rv.py
