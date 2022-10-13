import re
import os
from urllib.parse import urlparse


def get_domain(url):
    parse = urlparse(url)
    scheme = parse[0] + '://'
    host = parse[1]
    return scheme + host


def to_dir(dir, path_to_html):
    dir_name = path_to_html + '_files'
    full_path = os.path.join(dir, dir_name)
    return dir_name, full_path


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
