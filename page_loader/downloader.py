from page_loader.data_preparer import prepare_html_data_and_content
from page_loader.content_loader import get_html_data_and_path
from page_loader.content_loader import download_content
import logging


def download(url, dir):
    path_to_html, data = get_html_data_and_path(dir, url)
    html_data, content = prepare_html_data_and_content(data, url, dir)
    logging.info(f'write html file: {path_to_html}')
    with open(path_to_html, 'w+') as html_file:
        html_file.write(html_data)
    download_content(content)
    return path_to_html
