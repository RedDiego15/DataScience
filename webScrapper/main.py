import argparse
import logging

import news_pages_objects as news
logging.basicConfig(level = logging.INFO)
from common import config

logger = logging.getLogger(__name__)

def _news_scraper(news_site_uid):
    host = config()['news_sites'][news_site_uid]['url']

    logging.info('Begining scrapper for {}'.format(host))
    homepage = news.HomePage(news_site_uid,host)
    print(homepage.article_links)


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