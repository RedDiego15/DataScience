import scrapy

class QuotesSpider(scrapy.Spider):
    name='quotes' #esta variable tiene que llamarse name
    _start_urls =[
        'http://quotes.toscrape.com/'
    ]

    def parse(self,response):

        """define la logica a partir de la cual extraemos info"""
        with open('resultados.html','w+',encoding = 'utf-8') as f:
            f.write(response.text)




