from datetime import date
from unittest import result
import scrapy


class UkrainekeySpider(scrapy.Spider):
    name = 'ukrainekey'
    allowed_domains = ['ohchr.org']
    start_urls = ['https://www.ohchr.org/en/latest?field_geolocation_target_id%5B1136%5D=1136']

    def parse(self, response):

        article = response.xpath('//a[contains(@href,"/ukraine-civilian-casualty-update-")]')
        
        for lien in article:
            yield{
                'article_url' : lien.xpath('.//@href').get(),
                'article_date' : lien.xpath('.//p[@class="text--eyebrow card-2__eyebrow eyebrow-3"]/text()').get()
            }


        next = response.xpath('//li[@class="pager__item pager__item--next"]/a/@href').get()
        if next:
            new_url = response.urljoin(next)
            yield scrapy.Request(url=new_url,callback=self.parse)