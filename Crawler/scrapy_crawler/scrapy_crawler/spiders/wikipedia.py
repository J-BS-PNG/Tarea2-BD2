import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from w3lib.url import url_query_cleaner
import extruct


def processLinks(links):
    for link in links:
        link.url = url_query_cleaner(link.url)
        yield link
    

class wikipediaCrawler(CrawlSpider):
    name = 'wikipedia'
    allowed_domins = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Main_Page']
    rules = (
        Rule(LinkExtractor(), 
        process_links = processLinks,
        callback='parse_item',
        follow=True),
    )

    def parse_item(self, response):
        return {
            'url' : response.url,
            'metadata' : extruct.extract(
                response.text,
                response.url,
                syntaxes = ['opengraph', 'json-ld']
            ),
        }