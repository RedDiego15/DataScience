import argparse
import logging
import re  #importo el modulo de expresiones regulares

import datetime
import csv

from requests.exceptions import HTTPError
from urllib3.exceptions import MaxRetryError

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

is_Well_formed_link = re.compile(r'^https?://.+/.+$')
"""^ nos da el inicio de la palabra 
     r dice que es un string row
     es http con s opcional
     .+/ queremos una o mas letras y que termine en /
     $ significa terminar el patron"""
is_root_path = re.compile(r'^/.+$')

import news_pages_objects as news
from common import config

logger = logging.getLogger(__name__)

def _news_scraper(news_site_uid):
    host = config()['news_sites'][news_site_uid]['url']

    logging.info('Begining scrapper for {}'.format(host))
    homepage = news.HomePage(news_site_uid,host)

    articles = []
    for link in homepage.article_links:
        article = _fetch_article(news_site_uid,host,link)
        if article:
            logger.info('Article fetched!!!')
            articles.append(article)
            print("TITULO DEL ARTICULO: ",article.title)
        print(len(articles))
    _save_articles(news_site_uid,articles)

def _save_articles(news_site_uid, articles):
    now = datetime.datetime.now().strftime('%y_%m_%d')
    out_file_name = '{news_site_uid}_{datetime}_articles.csv'.format(
        news_site_uid = news_site_uid,
        datetime = now)
    # no podemos acceder a las propiedades por que add property no se refleja como propiedad
    # de python se refleja como funcion
    # vamos a filtrar todas las propiedades que no empiecen por guion bajo
    csv_headers = list(filter(lambda property: not property.startswith('_'),dir(articles[0])))
    with open(out_file_name,mode = 'w+') as f:
        writer = csv.writer()
        writer.writerow(csv_headers) #escribe la primera columna nuestros csv headers

        for article in articles:
            row = [str(getattr(article,prop))for prop in csv_headers]
            writer.writerow(row)

def _fetch_article(news_site_uid,host,link):
    logging.info('Start fetching article at {}'.format(link))
    article = None

    try:
        article = news.ArticlePage(news_site_uid,_build_link(host,link))
    except(HTTPError,MaxRetryError) as e:
        logger.warning("Error while fetching the article",exc_info = False)

    if article and not article.body:
        logger.warning('Invalid article. There is no body')
    return article

def _build_link(host,link):
    if is_Well_formed_link.match(link):
        return link
    elif is_root_path.match(link):
        return '{}{}'.format(host,link)
    else:
        return'{host}/{uri}'.format(host=host,uri = link)

if __name__ == '__main__':
    parser = argparse.ArgumentParser() #para decir que el programa recibe argumentos
    print(list(config().keys()))
    newSiteChoices = list(config()['news_sites'].keys())
    parser.add_argument('news_site',
                        help = 'The news site that you want to scrape',
                        type = str,
                        choices=newSiteChoices)

    args = parser.parse_args()
    _news_scraper(args.news_site)