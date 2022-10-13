from page_loader.html import process_html_data
from page_loader.url import generate_page_path, to_dir
from progress.bar import Bar
import requests
import logging
import os


def download_assets(assets):
    logging.info('Download files...')
    bar = Bar('Downloading:', max=len(assets))
    for asset in assets:
        url, path = asset
        with open(path, 'wb') as file:
            url_response = requests.get(url)
            url_response.raise_for_status()
            file.write(url_response.content)
        bar.next()
    bar.finish()
    logging.info('Downloading files successful!')


def download(url, dir):
    page_path = generate_page_path(url)
    path_to_html = f'{generate_page_path(url)}.html'
    path_to_html = os.path.join(dir, path_to_html)
    files_dir = to_dir(dir, page_path)

    logging.info(f'Requesting url: {url}')
    html_data, assets = process_html_data(url, files_dir)

    logging.info(f'output path: {os.path.abspath(dir)}')

    with open(path_to_html, 'w+') as html_file:
        html_file.write(html_data)
    logging.info(f'write html file: {path_to_html}')

    if not os.path.exists(files_dir[1]):
        os.mkdir(files_dir[1])
    download_assets(assets)
    return path_to_html
