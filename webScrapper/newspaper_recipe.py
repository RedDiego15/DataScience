import argparse
import logging
logging.basicConfig(level = logging.INFO)
from urllib.parse import urlparse
import pandas as pd
import hashlib

logger = logging.getLogger(__name__)
import nltk
from nltk.corpus import stopwords

#nltk.download('punkt') se debe ejecutar la primera vez si nunca se ha usado nltk
#nltk.download('stopwords') #palabras que no se usan

stopWords = set(stopwords.words('spanish'))
def main(filename):
    logger.info("Starting cleaning process")
    df = _read_data(filename)
    newspaper_uid = _extract_newspaper_uid(filename)
    df = _add_newspaper_uid_column(df,newspaper_uid)
    df = _extract_host(df)
    df = _delete_missing_entries(df)
    _delete_duplicates(df, 'title')
    _add_uid_row(df)
    _clean_title_dataFrame(df)
    _clean_body(df)
    df =  _tokenize_column(df, "title")
    _save_data(df,filename)
    return df



def _extract_newspaper_uid(filename):
    """Extrae el nombre del sitio de noticias"""
    logger.info('Exracting newspaper uid')
    newspaper_uid = filename.split('_')[0] #esto por como es el nombre de nuestro archivo eluniversal_2020_..
    logger.info('Newspaper uid detected: {}'.format(newspaper_uid))

    return newspaper_uid

def _read_data(filename):
    logger.info('Reading file {}'.format(filename))

    return pd.read_csv(filename)


def _add_newspaper_uid_column(df,newspaper_uid):
    logger.info('Filling newspaper_uid column with {}'.format(newspaper_uid))
    df['newspaper_uid'] = newspaper_uid
    return df

def _extract_host(df):
    """Extrae la fuente de donde salio la noticia"""
    logger.info('Extracting host from urls')
    df['host'] = df['url'].apply(lambda url: urlparse(url).netloc)
    return df


def _clean_title_dataFrame(df):
    logger.info('Filling missing titles')
    missingTitlesMask = df['title'].isna()
    missingTitles= (df[missingTitlesMask]['url']
                    .str.extract(r'(?P<missing_title>[^/]+)$') #importante darle un nombre de identificador a la columna en esete caso missing_title
                    .applymap(lambda title: title.replace("-"," ").capitalize())
                    )
    df.loc[missingTitlesMask,'title'] = missingTitles.loc[:,'missing_title']

def _add_uid_row(df):
    logger.info('Creando ids unicos para cada noticia')
    uids = (df
            .apply(lambda row: hashlib.md5(bytes(row['url'].encode())),axis=1)
            .apply(lambda hash_object: hash_object.hexdigest())
    )
    df['uid'] = uids
    df.set_index('uid',inplace=True) #linea necesaria o habria que retornar df
                                     #cada modificacion que hacemos a panda nos regresa otro dataFrame

def _clean_body(df):
    logger.info('Cleaning body of unnecessary characters')
    cleanBody = (df['body']
                    .apply(lambda row: row.strip("\n \r "))
                )
    df['body'] = cleanBody

def _tokenize_column(df,columnName):
    "return a data serie with the tokenize number for each row"
    logger.info('Tokenizing ',columnName)
    tokenize = (df[columnName]
           .dropna()
           .apply(lambda row: nltk.word_tokenize(row)) #tokenize all the words
           .apply(lambda tokens:list(filter(lambda token:token.isalpha(),tokens)))
           .apply(lambda tokens:map(lambda token:token.lower(),tokens)) #transformo a lower
           .apply(lambda wordList:list(filter(lambda word:word not in stopWords,wordList)))#filtro las palabras que no estan en la lista stopWords
           .apply(lambda valid_word_List: len(valid_word_List))
           )
    df['n_tokens_title'] = tokenize
    return df

def _delete_duplicates(df,columnName):
    logger.info('Removing duplicate entries')
    df.drop_duplicates(subset=[columnName],keep='first',inplace =  True)

def _delete_missing_entries(df):
    logger.info('Droping rows with missing values')
    return df.dropna()

def _save_data(df,filename):
    cleanFilename = 'clean_{}'.format(filename)
    logger.info('Saving data at location: {}'.format(cleanFilename))
    df.to_csv(cleanFilename)
    # df.to_csv(clean_filename, encoding = 'utf-8-sig')r


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename',
                        help= 'the path to the dirty data',
                        type=str)
    args = parser.parse_args()
    df = main(args.filename)

    print(df.iloc[:10,0:2])