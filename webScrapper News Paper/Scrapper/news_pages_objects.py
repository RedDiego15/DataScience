import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError
from urllib3.exceptions import MaxRetryError
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
            response.raise_for_status()  # arroja si la solicitud no se concluye correctamente
            if(response.status_code == 200):
                #response.request.header muestra la forma en como hago la solicitud
                self._html = BeautifulSoup(response.text, 'html.parser')

        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except MaxRetryError as Max_err:
            print(f'HTTP error MaxEntry ocurred: {Max_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6





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
        self._url = url

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

    @property
    def html(self):
        return self._html


