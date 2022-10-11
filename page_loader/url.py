import re
import os
from urllib.parse import urlparse
import logging


def get_domain(url):
    parse = urlparse(url)
    scheme = parse[0] + '://'
    host = parse[1]
    return scheme + host


def create_dir(dir, path_to_html):
    files_dir_name = path_to_html + '_files'
    files_dir_path = os.path.join(dir, files_dir_name)
    if not os.path.exists(files_dir_path):
        os.mkdir(files_dir_path)
    logging.info(f'output path: {files_dir_path}')
    return files_dir_name, files_dir_path


def to_file(url):
    url = ''.join(urlparse(url)[1:])
    if url[-1] == '/':
        url = url[:-1]
    path, ext = os.path.splitext(url)
    if not ext:
        path = re.split(r'\W+', path)
        path = '-'.join(path)
        return path + '.html'
    else:
        path = re.split(r'\W+', path)
        path = '-'.join(path)
        return path + ext


def generate_page_path(url):
    url = ''.join(urlparse(url)[1:])
    if url[-1] == '/':
        url = url[:-1]
    path, ext = os.path.splitext(url)
    if ext == '.html':
        path = re.split(r'\W+', path)
        path = '-'.join(path)
        return path
    full_path = re.split(r'\W+', url)
    return '-'.join(full_path)
