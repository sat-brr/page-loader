import re
import os
from urllib.parse import urlparse


def get_domain(url):
    parse = urlparse(url)
    scheme = parse[0] + '://'
    host = parse[1]
    return scheme + host


def to_dir(url):
    dir_path = generate_page_path(url) + '_files'
    return dir_path


def to_file(url):
    url, ext = os.path.splitext(url)
    file_path = generate_page_path(url)

    if ext:
        return file_path + ext
    return file_path + '.html'


def generate_page_path(url):
    url = url.strip('/')
    url = ''.join(urlparse(url)[1:])
    path, ext = os.path.splitext(url)
    if ext == '.html':
        path = re.split(r'\W+', path)
        path = '-'.join(path)
        return path
    full_path = re.split(r'\W+', url)
    return '-'.join(full_path)


#url = 'https://www.test.ru/123.txt'
#test1 = generate_page_path(url).split('-')
#print(to_file(url))
#print(pathlib.Path(url).name)