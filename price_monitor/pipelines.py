# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3

from price_monitor.price_alert import send_email


class PriceMonitorPipeline(object):

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect("price_monitor.db")
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""CREATE TABLE IF NOT EXISTS price_monitor  (
                url text,
                title,
                user text,
                email text,
                track_price integer,
                new_price integer,
                price_margin integer,
                PRIMARY KEY (url, email))""")

    def process_item(self, item, spider):

        self.get_db_data(item)
        return item

    def get_db_data(self, item):
        """ Search the database for an existing matching record based on url and email"""
        item = list(item.values())
        url = item[-1]
        email = item[-3]
        self.curr.execute("""select url, track_price, new_price, price_margin, email from price_monitor WHERE url=:url
                        and email=:email""",
                          {'url': url, 'email': email})
        rows = self.curr.fetchone()
        print("printing rows {}".format(rows))
        self.set_database(item, rows)

    def check_margin(self, item, rows):
        """ Check if the amount of the price drop is more than the price margin configured
            If the price drop is enough the price alert will get triggered"""
        price_margin = (float(rows[3]))
        track_price = rows[1]
        price = item[1]
        price = float(price.strip('$'))
        price_diff_percentage = price / track_price * 100
        price_drop = 100 - price_diff_percentage
        price_drop = round(price_drop, 2)
        price_diff_percentage = round(price_diff_percentage, 2)

        if 100 - price_margin >= price_diff_percentage:
            self.call_send_email(item, rows, price_diff_percentage, price_drop)

    def set_database(self, item, rows):
        """ Call insert or update database functions """
        url = item[-1]
        email = item[-3]
        scraped_price = (float(item[1]))
        if rows is not None:
            rows_url = rows[0]
            new_price = rows[1]
            if url == rows_url and email == rows[-1] and scraped_price != rows[1]:
                self.set_data_update(item, rows_url, new_price)
        self.check_margin(item, rows)

    def set_data_insert(self, item):
        """ Insert the scraped data into the database"""
        self.curr.execute(""" insert into price_monitor (url, title, user, email, track_price, new_price, price_margin)
                         values (?, ?, ?, ?, ?, ?, ?)""", (

             item[-1], item[0], item[2], item[3], item[1], item[1], item[-2]

         ))
        self.conn.commit()

    def set_data_update(self, item, rows_url, new_price):
        """ update the matching row in the database"""
        # track_price = new_price
        print("From set data update")
        new_price = item[1]
        self.curr.execute("""update price_monitor SET new_price=?
                         WHERE url=?""",
                           (new_price, rows_url))
        self.conn.commit()
        print("data updated")

    def call_send_email(self, item, rows, price_diff_percentage, price_drop):
        """ Call the send email function """
        send_email(self, item, rows, price_diff_percentage, price_drop)
        

