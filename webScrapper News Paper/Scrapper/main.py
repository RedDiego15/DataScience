import argparse
import logging

import Functions as Fn
from common import config
from news_pages_objects import HomePage

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)


def _news_scraper(news_site_uid):
    host = config()['news_sites'][news_site_uid]['url']
    logging.info('Begining scrapper for {}'.format(host))
    homepage = HomePage(news_site_uid,host)
    articles = Fn._getArticles(homepage,news_site_uid,host,logger)

    Fn._save_articles(news_site_uid,articles,logger)



if __name__ == '__main__':
    parser = argparse.ArgumentParser() #para decir que el programa recibe argumentos
    newSiteChoices = list(config()['news_sites'].keys())
    parser.add_argument('news_site',
                        help = 'The news site that you want to scrape',
                        type = str,
                        choices=newSiteChoices)

    args = parser.parse_args()
    _news_scraper(args.news_site)