import scrapy


class QuotesSpider(scrapy.Spider):
    #name es el nombre unico con el quescrapy se va a referir al spider
    name='quotes' #esta variable tiene que llamarse name
    start_urls =[
        "http://quotes.toscrape.com/"
    ]


    def parse(self,response):

        print("ENTRA A LA FUNCION PARSE")
        #with open('resultados.html', 'w', encoding='utf-8') as f:
        #    f.write(response.text)
        title = response.xpath('// h1 / a / text()').get()
        print("Title: {}".format(title))
        print("*" * 10, "\n")
        quotes = response.xpath('//span[@class="text" and @itemprop = "text"]/text()').getall()
        print("Quotes: ")
        for quote in quotes:
            print("Quote: {}".format(quote),"\n")
        print("*" * 10)
        topTenTags = response.xpath('//div[contains(@class,"tags-box")]/span[contains(@class,"tag-item")]/a/text()').getall()
        for tag in topTenTags:
            print("Tag: {}".format(tag), "\n")
        print("*" * 10)


