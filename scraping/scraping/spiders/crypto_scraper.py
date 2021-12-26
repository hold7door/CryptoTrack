
from datetime import datetime
from scrapy.http import Request
from scrapy.spiders import Spider

from collections import defaultdict

from scraping.settings import CRYPTOS
from scraping.spiders.dateParser import dateTimeFromString, getHoursDiff

class CryptoScraper(Spider):
    name = 'cryptos'
    start_urls = [
        'https://www.coindesk.com/'
    ]
    def parse(self, response):

        crypto_count = defaultdict(int)
        for crypto_name in CRYPTOS.keys():
            crypto_count[crypto_name] = 0
                    
        current_datetime = datetime.now()

        news_card_divs = response.xpath("//div[contains(@class, 'article-cardstyles')]")

        for d in news_card_divs:
            headline = d.xpath(".//a[contains(@class, 'headline')]/text()").extract()
            content = d.xpath(".//span[contains(@class, 'content-text')]/text()").extract()
            publish_date = d.xpath(".//div[contains(@class, 'ac-publishing-date')]/span/text()").extract()

            if len(publish_date) > 0:
                publish_date = publish_date[0]
                publish_date_obj = dateTimeFromString(publish_date)

                if publish_date_obj and getHoursDiff(publish_date_obj, current_datetime) < 1:
                    headline = headline[0] if len(headline) > 0 else ''
                    content = content[0] if len(content) > 0 else ''
                    headline_keywords = [w.lower() for w in  headline.split()]
                    content_keywords = [w.lower() for w in content.split()]
                    all_keywords = set(headline_keywords + content_keywords)
                    for crypto_name in CRYPTOS.keys():
                        for variants in CRYPTOS[crypto_name]:
                            if variants.lower() in all_keywords:
                                crypto_count[crypto_name] +=1
                   
            
        yield {
            'crypto_count': crypto_count,
            'instance_id': 1,
            'timestamp': current_datetime.timestamp()
        }

        