import datetime
import csv
import re  #importo el modulo de expresiones regulares
from news_pages_objects import ArticlePage


is_Well_formed_link = re.compile(r'^https?://.+/.+$')
"""^ nos da el inicio de la palabra 
     r dice que es un string row
     es http con s opcional
     .+/ queremos una o mas letras y que termine en /
     $ significa terminar el patron"""
is_root_path = re.compile(r'^/.+$')



def _getArticles(homepage, news_site_uid, host,logger):
    articles = []
    for link in homepage.article_links:
        print("El link: ",link)
        article = _fetch_article(news_site_uid, host, link,logger)
        if article:
            logger.info('Article fetched!!!')
            articles.append(article)
            print("TITULO DEL ARTICULO: ", article.title)
    print("el len de articles: ",len(articles))

    return articles


def _fetch_article(news_site_uid, host, link,logger):
    logger.info('Start fetching article at {}'.format(link))

    article = ArticlePage(news_site_uid, _build_link(host, link)) #aqui ya estoy en l;a pagina del link que obtuve del homepage
    if article:
        if article.html == None:
            logger.warning('html Error')
            article = None
        elif not article.body:
            logger.warning('Invalid article. There is no body')
            article = None
        elif not article.title:
            logger.warning('Invalid article. There is no Title')
            article = None

        return article


def _build_link(host, link):
    if is_Well_formed_link.match(link):
        return link
    elif is_root_path.match(link):
        return '{}{}'.format(host, link)
    else:
        return '{host}/{uri}'.format(host=host, uri=link)


def _save_articles(news_site_uid, articles ,logger):
    logger.info('Start Saving data')
    now = datetime.datetime.now().strftime('%Y_%m_%d')
    out_file_name = '{news_site_uid}_{datetime}_articles.csv'.format(
        news_site_uid=news_site_uid,
        datetime=now)


    # no podemos acceder a las propiedades por que add property no se refleja como propiedad
    # de python se refleja como funcion
    # vamos a filtrar todas las propiedades que no empiecen por guion bajo
    csv_headers = list(filter(lambda property: not property.startswith('_'), dir(articles[0])))
    csv_headers.remove('html')
    print("lista csvHeaders :",csv_headers)
    with open(out_file_name, mode='w+',encoding= "utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(csv_headers)  # escribe la primera columna nuestros csv headers

        for article in articles:
            print("Los atributos del articulo: ",(str(getattr(article, prop)) for prop in csv_headers))
            row = [str(getattr(article, prop)) for prop in csv_headers]
            writer.writerow(row)

    logger.info('Finish Saving data')