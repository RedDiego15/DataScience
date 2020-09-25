import scrapy


class QuotesSpider(scrapy.Spider):
    #name es el nombre unico con el quescrapy se va a referir al spider
    name='quotes' #esta variable tiene que llamarse name
    start_urls =[
        "http://quotes.toscrape.com/"
    ]

    #custom es una configuracion para guardar en json de forma automatica
    custom_settings = {
        'FEED_URI':'quotes.json',
        'FEED_FORMAT': 'json',
        'CONCURRENT_REQUESTS': 24, #scrapy realizara 24 peticiones a la vez
        'MEMUSAGE_LIMIT_MB':2048, #limite de la memoria ram que se permitira usar
        'MEMUSAGE_NOTIFY_MAIL':['diego-27ro@outlook.com'], #enviara un mensaje al mail si la memoria ram llega a pasarse del limite
        'ROBOTSTXT_OBEY':True,
        'USER_AGENT':'edge',
        'FEED_EXPORT_ENCODING':'utf-8',

    }

    def _get_quotes(self, response):
        quotes =  response.css('.quote')#response.xpath('//span[@class="text" and @itemprop = "text"]/text()').getall()
        quotes_list = []
        for quote in quotes:
            quotes_list.append({
                'text': quote.css('.text::text').get(),
                'author': quote.css('.author::text').get(),
                'tags': quote.css('.tags .tag::text').getall(),
            })
        return quotes_list

    def parse_only_quotes(self,response, **kwargs):
        if kwargs:
            quotes = kwargs['quotes']
            #response ahora apunta al nuevo url
            quotes.extend(self._get_quotes(response))
            yield(self._visit_page(response,kwargs))

    def _visit_page(self,response,data):
        # Importante preguntar si la variable next_page_button_link contiene algo
        # ya que por logica en algun momento llegariamos a ultima pagina.
        next_page_button_link = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page_button_link:
            # El metodo follow nos permite seguir al link (lo que hace scrapy es  dejar la url absoluta y cambiar el resto)
            # Este metodo posee un callback despues de haber cambiado de url.
            return response.follow(next_page_button_link, callback=self.parse_only_quotes, cb_kwargs=data)
        # scrapy permite multiples callbacks kwargs es un diccionario en el cual yo le paso argumentos a mi otra funcion
        return data






    def parse(self,response):
        title = response.xpath('// h1 / a / text()').get()
        topTags = response.xpath('//div[contains(@class,"tags-box")]/span[contains(@class,"tag-item")]/a/text()').getall()

        #pregunto si existe dentro de la ejeucion de este spider un atributo
        #de nombre top, voy a guardar ese resultado en mi variable top
        #sino existe(el atributo no se envio de ninguna manera) el resultado sera None
        top = getattr(self,'top',None) #pasar argumentos por consola

        if top:
            top = int(top)
            topTags = topTags[:top]

        data = {
            'title': title,
            'top_tags':topTags,
            'quotes': self._get_quotes(response)
        }

        yield self._visit_page(response,data)
        # with open('resultados.html', 'w', encoding='utf-8') as f:
        #    f.write(response.text)


