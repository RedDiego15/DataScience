import requests
from bs4 import BeautifulSoup

from common import config

class NewsPage:
    def __init__(self,idSitioNoticias,url):
        self._config = config()['news_sites'][idSitioNoticias]
        self._queries = self._config['queries']
        self._html = None
        self._visit(url)

    def _select(self, query_string):
        return self._html.select(query_string)

    def _visit(self, url):
        try:
            response = requests.get(url)
            #response.request.header muestra la forma en como hago la solicitud
            response.raise_for_status()  # arroja si la solicitud no se concluye correctamente
            self._html = BeautifulSoup(response.text, 'html.parser')
        except:
            self._html.bs4.BeautifulSoup('')


class HomePage(NewsPage):

    def __init__(self,idSitioNoticias,url):
        super().__init__(idSitioNoticias,url)

    @property
    def article_links(self):
        link_list = []
        for link in self._select(self._queries['homepage_article_links']): ##accedo al diccionario y selecciono
            if link and link.has_attr('href') and link['href'].startswith("http"):
                link_list.append(link)
        return set(link['href'] for link in link_list)

class ArticlePage(NewsPage):

    def __init__(self,news_site_uid,url):
        super().__init__(news_site_uid,url)

    #En web scrapp hay que ser muy defensivos

    @property
    def body(self):
        result = self._select(self._queries['article_body']) #en el archivo config tengo el atributo css para encontrar el texto del body
        #print("EL RESULT DE BODY: ",result)

        return result[0].text if len(result) else ''
    @property
    def title(self):
        result = self._select(self._queries['article_title'])
        #print("EL RESULT DE TITLE: ", result)
        if (len(result) > 0):
            print("EL RESULT DE TITLE[0].text: ", result[0].text)
        return result[0].text if len(result) else ''

    @property
    def url(self):
        return self._url


