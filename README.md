# price_monitor
Price monitor program for amazon
Reads a json file, with url to scrape, name, email, and configurable price margin
Scrapes the url from the json file from amazon only, and inserts that into a sqlite DB
The user will be notifed by email if the price has dropped below or equal to the price margin set in the json file

Prerequisites
* Python (Tested on python 3.6.5)
* scrapy

Installation Instructions
* Install python 
* Install python virtual environment
* Install requirements.txt
    * pip install -r requirements.txt
* Create the sqlite DB in the scrapy root directory
* Create the amazon_products json file price_monitor directory
* The email is sent through gmail. Go into gmail settings and Check Allow Less Secure Apps - 'On'
