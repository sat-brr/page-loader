from page_loader.html import process_html_data
from page_loader.url import generate_page_path, to_dir
from progress.bar import Bar
import requests
import logging
import os


def download_assets(assets, dir, url):
    assets_dir_path = os.path.join(dir, to_dir(url))

    if not os.path.exists(assets_dir_path):
        os.mkdir(assets_dir_path)

    logging.info('Download files...')
    bar = Bar('Downloading:', max=len(assets))
    for asset in assets:
        url, path_to_file = asset
        path_to_file = os.path.join(assets_dir_path, path_to_file)

        with open(path_to_file, 'wb') as file:
            url_response = requests.get(url)
            url_response.raise_for_status()
            file.write(url_response.content)
        bar.next()
    bar.finish()
    logging.info('Downloading files successful!')


def download(url, dir):
    logging.info(f'Requesting url: {url}')
    html_data, assets = process_html_data(url)

    logging.info(f'output path: {os.path.abspath(dir)}')

    path_to_html = f'{generate_page_path(url)}.html'
    path_to_html = os.path.join(dir, path_to_html)

    with open(path_to_html, 'w+') as html_file:
        html_file.write(html_data)
    logging.info(f'write html file: {path_to_html}')

    download_assets(assets, dir, url)
    return path_to_html
