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
    name = 'wiki'
    allowed_domins = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Main_Page']
    rules = (
        Rule(LinkExtractor(), 
        process_links = processLinks,
        callback='parse_item',
        follow=True),
    )

    # response.css('div.mw-body h1.firstHeading::text').get() *Titulos*
    # response.css('div.mw-body .mw-headline::text').getall() *Subtitulos* 
    # response.css('div.mw-body p::text').getall()  
    # response.css('div.mw-body .image img::attr(src)').getall() *Imagenes*
    # response.css('div.mw-body .image img::attr(alt)').extract()  *alt* 
    # response.css('div.mw-body div.mw-references-columns ol.references span.reference-text a::attr(href)').getall() *referencias*
    # response.css('div.mw-body div.references-column-width ol.references span.reference-text a::text').extract()  *referencias* 
    def parse_item(self, response):
        return {
            'title<Span>': response.css('div.mw-body h2 span.mw-headline::text').getall(), #*Titulos*
            'subtitulo<Span>': response.css('div.mw-body h3 span.mw-headline::text').getall(), #*Subtitulos* 
            'text<p>': response.css('div.mw-body p::text').getall(),  # *Contenido*
            'imagenes<img>': response.css('div.mw-body .image img::attr(src)').getall(), #*Imagenes*
            'alt<img>':response.css('div.mw-body .image img::attr(alt)').getall(),  #*alt* 
        }