from bs4 import BeautifulSoup
from urllib.parse import urlparse
from page_loader.url import to_file, get_domain
import requests
import os


TAGS = {'img': 'src', 'link': 'href', 'script': 'src'}


def process_html_data(url, dir):
    url_response = requests.get(url)
    url_response.raise_for_status()

    domain = get_domain(url)
    soup = BeautifulSoup(url_response.text, 'html.parser')
    dir_name, dir_path = dir

    assets = []
    for tag, attribute in TAGS.items():
        for source in soup(tag):
            source_url = source[attribute]
            domain_lnk = get_domain(source_url)

            if domain_lnk == domain or domain_lnk == '://':
                source_url = ''.join(urlparse(source_url)[2:])
                source_url = domain + source_url
                local_file_path = to_file(source_url)
                full_path_to_file = os.path.join(dir_path, local_file_path)
                assets.append((source_url, full_path_to_file))
                source[attribute] = os.path.join(dir_name, local_file_path)
    html_data = soup.prettify()
    return html_data, assets
