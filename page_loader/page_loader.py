import requests
import os
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import logging
from progress.bar import Bar
TAGS = ('img', 'link', 'script')


logger = logging.getLogger('page-loader')
logger.setLevel(logging.INFO)
f = logging.Formatter("%(levelname)s | %(name)s | %(message)s")
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
sh.setFormatter(f)
logger.addHandler(sh)


class KnownError(Exception):
    pass


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
    new_dir = make_path(url, dir=True)
    full_path = f'{dir}/{new_dir}'
    logger.info(f'Directory {full_path} creating...')
    try:
        os.mkdir(full_path)
        logger.info('Directory created')
    except FileExistsError:
        logger.warning('Directory exists')
    return new_dir, full_path


def get_files(page, url, dir):
    new_dir, full_path = make_dir(dir, url)
    logger.info('Download files...')
    domain = get_domain(url)
    open_page = open(page)
    soup = BeautifulSoup(open_page, 'html.parser')
    elements = find_by_tag(soup)
    bar = Bar('Downloading:', max=len(elements))
    for element in elements:
        elem_url, key = get_element_url(element)
        domain_lnk = get_domain(elem_url)
        if domain_lnk == domain or domain_lnk == '://':
            elem_url = ''.join(urlparse(elem_url)[2:])
        else:
            continue
        full_url = domain + elem_url
        local_path_file = make_path(full_url, file=True)
        full_path_to_file = f'{full_path}/{local_path_file}'
        with open(full_path_to_file, 'wb') as file:
            try:
                file.write(requests.get(full_url).content)
            except Exception:
                logger.warning(f'Download file ({full_url}) fail !!!')
        bar.next()
        element[key] = f"{new_dir}/{local_path_file}"
    saved_changes = soup.prettify()
    open_page.close()
    open_page = open(page, 'r+')
    open_page.write(saved_changes)
    open_page.close()
    bar.finish()
    logger.info('Downloading files successful!')


def create_html_file(dir, url):
    try:
        logger.info(f'Requesting url: {url}')
        data = requests.get(url)
        data.raise_for_status()
        path = f'{dir}/{make_path(url)}.html'
        with open(path, 'w+') as file:
            file.write(data.text)
        logger.info(f'Write html file: {path}')
        return path
    except (requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError,
            requests.exceptions.Timeout) as err:
        logger.error(f'Connection error from "{url}". Errcode: {err}')
        raise KnownError() from err
    except requests.exceptions.MissingSchema as err:
        logger.error(f'Invalid URL {url}: No scheme supplied.')
        raise KnownError() from err


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
    if ext == '.html' and file is True:
        path = re.split(r'\W+', path)
        path = '-'.join(path)
        return path + ext
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


def download(url, dir):
    try:
        open(dir, 'r')
        logger.error('Invalid directory path specified!')
        raise KnownError()
    except (FileNotFoundError, PermissionError) as err:
        logger.error("Directory does not exist or access denied. "
                     f'Error code: {err}')
        raise err
    except IsADirectoryError:
        pass
    path_to_url = create_html_file(dir, url)
    get_files(path_to_url, url, dir)
    logger.info(f"Page was downloaded as '{path_to_url}'.")
    return path_to_url
