import requests
from progress.bar import Bar
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import logging
from page_loader.work_with_urls import make_dir, make_path, get_domain


TAGS = {'img': 'src', 'link': 'href', 'script': 'src'}
logger = logging.getLogger('page-loader')


def find_by_tag(parse):
    result = {}
    for key, value in TAGS.items():
        url = parse.find_all(key, {value: True})
        if value not in result:
            result.setdefault(value, url)
        else:
            result[value].extend(url)
    return result


def download_file(source):
    logger.info('Download files...')
    bar = Bar('Downloading:', max=len(source))
    for url, path in source.items():
        with open(path, 'wb') as file:
            data = requests.get(url).content
            file.write(data)
        bar.next()
    bar.finish()
    logger.info('Downloading files successful!')


def get_files(page, url, dir):
    new_dir, full_path = make_dir(dir, url)
    domain = get_domain(url)
    open_page = open(page)
    soup = BeautifulSoup(open_page, 'html.parser')
    elements = find_by_tag(soup)
    urls_for_downloading = {}
    for atr, elem in elements.items():
        for source in elem:
            source_url = source[atr]
            domain_lnk = get_domain(source_url)
            if domain_lnk == domain or domain_lnk == '://':
                source_url = ''.join(urlparse(source_url)[2:])
            else:
                continue
            source_url = domain + source_url
            local_path_file = make_path(source_url, file=True)
            full_path_to_file = f'{full_path}/{local_path_file}'
            urls_for_downloading.setdefault(source_url, full_path_to_file)
            source[atr] = f"{new_dir}/{local_path_file}"
    download_file(urls_for_downloading)
    saved_changes = soup.prettify()
    open_page.close()
    return saved_changes
