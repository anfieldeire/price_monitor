import scrapy
import json
from ..items import AmazonItem


class MySpider(scrapy.Spider):
    name = 'price_monitor'

    def start_requests(self):
        with open('C:\\Users\\hassy\\Documents\\python_venv\\price_monitor\\price_monitor\\amazon_products.json') as f:
            data = json.load(f)
            itemdatalist = data['itemdata']
            for item in itemdatalist:
                yield scrapy.Request(url=item['url'], callback=self.parse, meta={'item': item}) 

    def parse(self, response):
        item = response.meta["item"]
        scrapeitem = AmazonItem()
        title = response.css('span#productTitle::text').extract_first()
        title = title.strip()
        price = response.css('span#priceblock_ourprice::text').extract_first()
        scrapeitem['title'] = title
        scrapeitem['price'] = price.strip('$')
        scrapeitem['name'] = item["name"] # from response.meta
        scrapeitem['email'] = item["email"] # from response.meta
        scrapeitem['price_margin'] = item["price_margin"]
        scrapeitem['url'] = item['url']
        yield scrapeitem

