import re
import os
from urllib.parse import urlparse
from page_loader.scripts.page_load import logger


def make_dir(dir, url):
    new_dir = make_path(url, dir=True)
    full_path = f'{dir}/{new_dir}'
    logger.info(f'Directory {full_path} creating...')
    try:
        os.mkdir(full_path)
        logger.info('Directory created')
    except FileExistsError:
        logger.warning('Directory exists')
    return new_dir, full_path


def make_path(url, file=False, dir=False):
    url = ''.join(urlparse(url)[1:])
    if url[-1] == '/':
        url = url[:-1]
    path, ext = os.path.splitext(url)
    if not ext and file is True:
        path = re.split(r'\W+', path)
        path = '-'.join(path)
        return path + '.html'
    if ext == '.html':
        path = re.split(r'\W+', path)
        path = '-'.join(path)
        return path
    if file:
        path = re.split(r'\W+', path)
        path = '-'.join(path)
        return path + ext
    if dir:
        path += ext
        path = re.split(r'\W+', path)
        path = '-'.join(path)
        return path + '_files'
    full_path = re.split(r'\W+', url)
    return '-'.join(full_path)
