import requests
import bs4

from common import config

"""class NewsPage:
    def __init__(self,idSitioNoticias,url):
        self._config = config()['news_sites'][idSitioNoticias]
        self._queries = self._config['queries']
        self._html = None
        self._visit(url)
"""

class HomePage():
    
    def __init__(self,idSitioNoticias,url):
        self._config = config()['news_sites'][idSitioNoticias]
        self._queries = self._config['queries']
        self._html = None

        self._visit(url)
        #super().__init__(idSitioNoticias,url)

    @property
    def article_links(self):
        link_list = []
        for link in self._select(self._queries['homepage_article_links']): ##accedo al diccionario
            if link and link.has_attr('href'): # select me retorna un objeto, revisar que atributos y metodos tienen los objetos que retorna select
                link_list.append(link)
        print(link_list)
        return set(link_list)

    def _select(self,query_string):
        return self._html.select(query_string)

    def _visit(self,url):
        response = requests.get(url)
        response.raise_for_status() #arroja si la solicitud no se concluye correctamente

        self._html = bs4.BeautifulSoup(response.text,'html.parser')