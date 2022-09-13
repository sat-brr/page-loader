from page_loader.download_files import get_files
from page_loader.write_html import create_html_file
import logging


logger = logging.getLogger('page-loader')


def edit_html(html_file, changes):
    with open(html_file, 'r+') as file:
        file.write(changes)


def download(url, dir):
    path_to_html = create_html_file(dir, url)
    changes = get_files(path_to_html, url, dir)
    edit_html(path_to_html, changes)
    logger.info(f"Page was downloaded as '{path_to_html}'.")
    return path_to_html
