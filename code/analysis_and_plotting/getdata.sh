#!/bin/bash

cd ../scrapers

#python3 precipitation-emo.py
python3 recessions-emo.py
python3 wbdata.py


cd ../temperature

python3 scraper_temp_rv.py
