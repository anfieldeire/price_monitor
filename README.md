# price_monitor
Price monitor program for amazon

The program reads a json file, with url to scrape, name, email, and configurable price margin

Scrapes the url from the json file from amazon only, and inserts the price plus user info into a sqlite DB

The user will be notifed by email if the price has dropped below or equal to the price margin set in the json file

Prerequisites
* Python (Tested on python 3.6.5)
* scrapy
* sqlite

Installation Instructions
* Install python 
* Install python virtual environment
* Install requirements.txt
    * pip install -r requirements.txt
* Create the sqlite DB in the scrapy root directory
* Create the amazon_products json file
* The email is sent through gmail. To send the email. Go into gmail settings and Check Allow Less Secure Apps - 'On'

Running the program
* Create the virtual environment and activate
   * For example in windows ->  windows_virtualenv/price_monitor/Scripts/activate.bat
   * Create the scrapy project
      *  cd into windows_virtualenv/price_monitor and run scrapy startproject price_monitor
   * Run scrapy like so - from windows_virtualenv/price_monitor command line, run scrapy crawl price_monitor
