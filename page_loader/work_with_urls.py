import re
import os
from urllib.parse import urlparse
import logging


logger = logging.getLogger('page-loader')


def get_domain(url):
    parse = urlparse(url)
    scheme = parse[0] + '://'
    host = parse[1]
    return scheme + host


def make_dir(dir, url):
    new_dir = make_path(url, dir=True)
    full_path = f'{dir}/{new_dir}'
    logger.info(f'Directory {full_path} creating...')
    if os.path.exists(full_path):
        logger.info('Directory exists')
    else:
        os.mkdir(full_path)
        logger.info('Directory created')
    return new_dir, full_path


def make_path_to_file(path, ext):
    if not ext:
        path = re.split(r'\W+', path)
        path = '-'.join(path)
        return path + '.html'
    else:
        path = re.split(r'\W+', path)
        path = '-'.join(path)
        return path + ext


def make_path_to_dir(path, ext):
    path += ext
    path = re.split(r'\W+', path)
    path = '-'.join(path)
    return path + '_files'


def make_path(url, file=False, dir=False):
    url = ''.join(urlparse(url)[1:])
    if url[-1] == '/':
        url = url[:-1]
    path, ext = os.path.splitext(url)
    if file:
        return make_path_to_file(path, ext)
    if dir:
        return make_path_to_dir(path, ext)
    if ext == '.html':
        path = re.split(r'\W+', path)
        path = '-'.join(path)
        return path
    full_path = re.split(r'\W+', url)
    return '-'.join(full_path)
