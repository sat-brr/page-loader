import requests
import logging
from page_loader.work_with_urls import make_path
import os


logger = logging.getLogger('page-loader')


def get_data(url):
    logger.info(f'Requesting url: {url}')
    data = requests.get(url)
    data.raise_for_status()
    return data


def write_to_file(path, data):
    logger.info(f'Write html file: {path}')
    with open(path, 'w+') as file:
        file.write(data.text)


def create_html_file(dir, url):
    data = get_data(url)
    url_to_path = f'{make_path(url)}.html'
    full_path = os.path.join(dir, url_to_path)
    write_to_file(full_path, data)
    return full_path
