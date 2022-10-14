from bs4 import BeautifulSoup
from urllib.parse import urlparse
from page_loader.url import to_dir, to_file, get_domain
import requests
import os


TAGS = {'img': 'src', 'link': 'href', 'script': 'src'}


def process_html_data(url):
    url_response = requests.get(url)
    url_response.raise_for_status()

    domain = get_domain(url)
    soup = BeautifulSoup(url_response.text, 'html.parser')
    assets_dir_name = to_dir(url)

    assets = []
    for tag, attribute in TAGS.items():
        for source in soup(tag):
            source_url = source[attribute]
            domain_lnk = get_domain(source_url)

            if domain_lnk == domain or domain_lnk == '://':
                source_url = ''.join(urlparse(source_url)[2:])
                source_url = domain + source_url
                path_to_file = to_file(source_url)
                assets.append((source_url, path_to_file))
                source[attribute] = os.path.join(assets_dir_name, path_to_file)
    html_data = soup.prettify()
    return html_data, assets
