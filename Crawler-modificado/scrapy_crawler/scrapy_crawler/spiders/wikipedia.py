import struct
import json
from string import punctuation
type(punctuation)
import nltk
#nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from w3lib.url import url_query_cleaner

# ejecutar scrapy crawl wiki -o wikipedia.json -s DEPTH_LIMIT=1
file = open('data_wiki.txt', 'w')
print(stopwords.words('english'))
def processLinks(links):
    for link in links:
        link.url = url_query_cleaner(link.url)
        yield link

class wikipediaCrawler(CrawlSpider):
    name = 'wiki'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Wikipedia']
    rules = (
        Rule(LinkExtractor(), 
        process_links = processLinks,
        callback='parse',
        follow=True),
    )


    def parse(self, response):
    
        #extrae el contenido de la pagina con el css sleectors y lo pasa a texto
        vURL = response.url#url
        vTitle = response.css('.mw-body h2 span.mw-headline::text').getall() #*Titulos*
        vSubtitulo1 = response.css('.mw-body h3 span.mw-headline::text').getall() #*Subtitulos* 
        vSubtitulo2 = response.css('.mw-body h4 span.mw-headline::text').getall() #*Subtitulos* 
        vSubtitulo3 = response.css('.mw-body h5 span.mw-headline::text').getall() #*Subtitulos* 
        vText = response.css('.mw-body p::text').getall() # *Contenido*
        vImagenes =  response.css('.mw-body .image img::attr(src)').getall() #*Imagenes*
        vAlt = response.css('.mw-body .image img::attr(alt)').getall()  #*alt* 
        vReferences = response.css('div.mw-body ol.references a::attr(href)').getall()
        #print(vReferences)
        
        #Prepara los titulos
        vTitle = removeTitles(vTitle)
        vTitle = ' + '.join(vTitle)
        vTitle = vTitle.replace('-', '')
        vTitle = vTitle.split(' + ')
        #print(vTitle)

        #Prepara los subtitulos
        vSubtitlulo = vSubtitulo1 + vSubtitulo2 + vSubtitulo3
        vSubtitlulo = ' + '.join(vSubtitlulo)
        vSubtitlulo = vSubtitlulo.replace('-', '')
        vSubtitlulo = vSubtitlulo.split(' + ')
        #print(vSubtitlulo)


        #Preparar alt
        vAlt = ' + '.join(vAlt)
        vAlt = vAlt.replace('-', '')
        vAlt = vAlt.split(' + ')
        #print(vAlt)

        #Filtra las palabras y quita signos de puntuacion
        vTitle = filterWords(' - '.join(vTitle))
        vSubtitulo = filterWords(' - '.join(vSubtitlulo))
        vText = filterWords(' '.join(vText))
        vAlt = filterWords(' - '.join(vAlt))
        #print(vTitle)




        #Stem words
        vTitle = stemWords(vTitle)
        vSubtitulo = stemWords(vSubtitulo)
        vText = stemWords(vText)
        vAlt = stemWords(vAlt)
        #print(vTitle)


        
       
        scraped_info = {
                'url' : vURL,
                'title': ' '.join(vTitle),
                'subtitle': ' '.join(vSubtitulo),
                'content': ' '.join(vText),
                'images': ' - '.join(vImagenes), 
                'alt': ' '.join(vAlt),
                'references': ' '.join(vReferences)
        }


        file.write(str(scraped_info)+"\n")
        #yield scraped_info


def removePunctuation(data):
    punctuation = '!"#$%&()*+,.:;<=>?@[\]^_`{|}~/'
    for p in data:
        if p in punctuation:
            data = data.replace(p, '')
    return data

def removeTitles(data):
    if 'See also' in data:
        data.remove('See also')
    if 'References'in data:        
        data.remove('References')
    if 'Further reading' in data:
        data.remove('Further reading')
    if 'External links'in data:
        data.remove('External links')
    if 'Notes' in data:
        data.remove('Notes')
    return data

def filterWords(data):
    data = removePunctuation(data)
    data.lower()
    data = data.split()
    stopwordsList = stopwords.words('english') 
    data_filtered = [w for w in data if not w.lower() in stopwordsList]

    return data_filtered


def stemWords(data):
    stem_data = []
    ps = PorterStemmer()
    for word in data:
        if word == '-':
            stem_data.append( '-')
        else:
            stem_data.append( ps.stem(word))
            #print(word + '->' + ps.stem(word))
        #print(word + '->' + ps.stem(word))
        #print(stem_data)
    return stem_data