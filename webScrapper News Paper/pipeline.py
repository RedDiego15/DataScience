import logging
logging.basicConfig(level = logging.INFO)
import subprocess #permite manipular archivos de terminal
import os
import shutil

logger = logging.getLogger(__name__)

news_sites_uids = ['eluniversa','elpais']

def main():
    logger.info('Starting ETL process')
    _extract()
    _transform() # ejecuta la receta para limpiar los datos
    _load() #lo carga a la base de datos
    logger.info('ETL process finished')
def _extract():
    logger.info('Starting extract process')
    for news_site_uid in news_sites_uids:
        subprocess.run(['python','main.py',news_site_uid],cwd='./extract') #cwd ejecuta esto ene l current worker directory
        path = '.\\extract'
        file = _search_file(path, news_site_uid)
        _move_file(path + '\\' + file, '.\\transform\\' + file)



def _search_file(path, file_match):
    logger.info('Searching file')
    for rutas in list(os.walk(path))[0]:
        for file in rutas:
            if file_match in file:
                return file
    return None

def _move_file(origen, destino):
    logger.info('Moving file')
    shutil.move(origen, destino)

def _transform():
    logger.info('Starting transform process')
    for news_site_uid in news_sites_uids:
        dirty_data_filename = _search_file('.\\transform', news_site_uid)
        clean_data_filename = f'clean_{dirty_data_filename}'
        subprocess.run(['python', 'newspaper_receipe.py', dirty_data_filename], cwd='./transform')
        _remove_file('.\\transform', dirty_data_filename)
        _move_file('.\\transform\\' + clean_data_filename, '.\\load\\' + clean_data_filename)

def _remove_file(path, file):
    logger.info(f'Removing file {file}')
    os.remove(f'{path}\\{file}')

def _load():
    logger.info('Starting load process')
    for news_site_uid in news_sites_uids:
        clean_data_filename = _search_file('.\\load', news_site_uid)
        subprocess.run(['python', 'load_db.py', clean_data_filename], cwd='./load')
        _remove_file('.\\load', clean_data_filename)

if __name__ == '__main__':
    main()
