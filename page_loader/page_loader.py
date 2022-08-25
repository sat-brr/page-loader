import requests
import os
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def get_files(page, url, dir):
    dir_name = f'{dir}/{make_path(url, dir=True)}'
    os.mkdir(dir_name)
    domain = get_domain(url)
    open_page = open(page)
    soup = BeautifulSoup(open_page, 'html.parser')
    files = soup.find_all('img')
    for element in files:
        lnk = element['src']
        lnk = ''.join(urlparse(lnk)[2:])
        full_lnk = domain + lnk
        path_to_file = f'{dir_name}/{make_path(full_lnk, file=True)}'
        with open(path_to_file, 'wb') as rr:
            rr.write(requests.get(full_lnk).content)
        element['src'] = path_to_file
    saved_changes = soup.prettify()
    open_page.close()
    open_page = open(page, 'r+')
    open_page.write(saved_changes)
    open_page.close()


def create_html_file(dir, url):
    data = requests.get(url).text
    path = f'{dir}/{make_path(url)}.html'
    with open(path, 'w+') as file:
        file.write(data)
    return path


def get_domain(url):
    parse = urlparse(url)
    scheme = parse[0] + '://'
    host = parse[1]
    return scheme + host


def make_path(url, file=False, dir=False):
    url = ''.join(urlparse(url)[1:])
    if url[-1] == '/':
        url = url[:-1]
    path, ext = os.path.splitext(url)
    if ext == '.html':
        path = re.split(r'\W+', path)
        path = '-'.join(path)
        return re.split(r'\W+', path)
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


def download(dir, url):
    path_to_url = create_html_file(dir, url)
    get_files(path_to_url, url, dir)
    return path_to_url
