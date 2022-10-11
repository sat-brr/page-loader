from page_loader.handler import process_html_data
from progress.bar import Bar
import requests
import logging


def download(url, dir):
    logging.info(f'Requesting url: {url}')
    html_data, assets, html_path = process_html_data(url, dir)
    logging.info(f'write html file: {html_path}')
    with open(html_path, 'w+') as html_file:
        html_file.write(html_data)

    logging.info('Download files...')
    bar = Bar('Downloading:', max=len(assets))
    for asset in assets:
        url, path = asset
        with open(path, 'wb') as file:
            data = requests.get(url)
            data.raise_for_status()
            file.write(data.content)
        bar.next()
    bar.finish()
    logging.info('Downloading files successful!')
    return html_path
