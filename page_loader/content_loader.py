import requests
import logging
import os
from progress.bar import Bar
from page_loader.url_handler import make_path


def get_html_data_and_path(dir, url):
    logging.info(f'Requesting url: {url}')
    data = requests.get(url)
    data.raise_for_status()
    url_to_path = f'{make_path(url)}.html'
    full_path = os.path.join(dir, url_to_path)
    return full_path, data.text


def download_content(source):
    logging.info('Download files...')
    bar = Bar('Downloading:', max=len(source))
    for element in source:
        url, path = element
        with open(path, 'wb') as file:
            data = requests.get(url).content
            file.write(data)
        bar.next()
    bar.finish()
    logging.info('Downloading files successful!')
