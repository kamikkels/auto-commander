#!/bin/bash
# update script for card sources

wget http://mtgjson.com/json/AllSets.json.zip
unzip AllSets.json.zip
mv AllSets.json sources
python cardloader.py

