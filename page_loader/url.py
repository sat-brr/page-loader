import re
import os
from urllib.parse import urlparse


def get_domain(url):
    parse = urlparse(url)
    scheme = parse[0] + '://'
    host = parse[1]
    return scheme + host


def to_dir(url):
    path = ''.join(urlparse(url)[1:])
    if url[-1] == '/':
        url = url[:-1]
    path = re.split(r'\W+', path)
    path = '-'.join(path)
    return path + '_files'


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
