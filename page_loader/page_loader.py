import requests
import os
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import logging


TAGS = ('img', 'link', 'script')


class KnownError(Exception):
    pass


def create_log_file():
    logging.basicConfig(level=logging.INFO)
    logging.StreamHandler()


def find_by_tag(parse):
    result = []
    for tag in TAGS:
        if tag == 'link':
            found = parse.find_all(tag, href=True)
            result.extend(found)
            continue
        found = parse.find_all(tag, src=True)
        result.extend(found)
    return result


def get_element_url(elem):
    try:
        elem_url = elem['src']
        return elem_url, 'src'
    except KeyError:
        elem_url = elem['href']
        return elem_url, 'href'


def make_dir(dir, url):
    dir_path = f'{dir}/{make_path(url, dir=True)}'
    logging.info(f'Directory {dir_path} creating...')
    try:
        os.mkdir(dir_path)
        logging.info('Directory created')
    except FileExistsError:
        logging.info('Directory exists')
    return dir_path


def get_files(page, url, dir):
    logging.info('Download files...')
    dir_path = make_dir(dir, url)
    domain = get_domain(url)
    open_page = open(page)
    soup = BeautifulSoup(open_page, 'html.parser')
    elements = find_by_tag(soup)
    for element in elements:
        elem_url, key = get_element_url(element)
        domain_lnk = get_domain(elem_url)
        if domain_lnk == domain or domain_lnk == '://':
            elem_url = ''.join(urlparse(elem_url)[2:])
        else:
            continue
        full_url = domain + elem_url
        path_to_file = f'{dir_path}/{make_path(full_url, file=True)}'
        with open(path_to_file, 'wb') as file:
            try:
                file.write(requests.get(full_url).content)
            except Exception:
                logging.error(f'Download file ({full_url}) fail !!!')
        element[key] = path_to_file
    saved_changes = soup.prettify()
    open_page.close()
    open_page = open(page, 'r+')
    open_page.write(saved_changes)
    open_page.close()
    logging.info('Downloading files successful')


def create_html_file(dir, url):
    logging.info('Loading page...')
    try:
        data = requests.get(url).text
        path = f'{dir}/{make_path(url)}.html'
        with open(path, 'w+') as file:
            file.write(data)
        logging.info('Loading page success.')
    except requests.ConnectionError as err:
        raise KnownError('Connection fail') from err
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
    if file:
        path = re.split(r'\W+', path)
        path = '-'.join(path)
        return path + ext
    if dir:
        path += ext
        path = re.split(r'\W+', path)
        path = '-'.join(path)
        return path + '_files'
    if ext == '.html':
        path = re.split(r'\W+', path)
        path = '-'.join(path)
        return re.split(r'\W+', path)
    full_path = re.split(r'\W+', url)
    return '-'.join(full_path)


def download(dir, url):
    create_log_file()
    path_to_url = create_html_file(dir, url)
    get_files(path_to_url, url, dir)
    logging.info(f"Page was downloaded as '{path_to_url}'.")
