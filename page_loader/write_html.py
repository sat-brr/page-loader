import requests
from page_loader.scripts.page_load import logger
from page_loader.work_with_paths import make_path


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
        raise err
    except requests.exceptions.MissingSchema as err:
        logger.error(f'Invalid URL {url}: No scheme supplied.')
        raise err
