import scrapy
# ejecutar scrapy crawl wiki -o wikipedia.json -s DEPTH_LIMIT=1
class BlogSpider(scrapy.Spider):
    name = 'wikipedia'
    allowed_domins = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Main_Page'] # https://en.wikipedia.org/wiki/Pyramid_of_Sahure

    def parse(self, response):
       yield{
            'title<Span>': response.css('div.mw-body h2 span.mw-headline::text').getall(), #*Titulos*
            'subtitulo<Span>': response.css('div.mw-body h3 span.mw-headline::text').getall(), #*Subtitulos* 
            'text<p>': response.css('div.mw-body p::text').getall(),  # *Contenido*
            'imagenes<img>': response.css('div.mw-body .image img::attr(src)').getall(), #*Imagenes*
            'alt<img>':response.css('div.mw-body .image img::attr(alt)').getall(),  #*alt* 
       }
       for a in response.css('div.mw-body p a'):
            yield response.follow(a, callback=self.parse)
       



    