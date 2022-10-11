from bs4 import BeautifulSoup
from urllib.parse import urlparse
from page_loader.url import create_dir, to_file, get_domain, generate_page_path
import requests
import os


TAGS = {'img': 'src', 'link': 'href', 'script': 'src'}


def process_html_data(url, dir):
    page_data = requests.get(url)
    page_data.raise_for_status()
    local_path_to_page = generate_page_path(url)
    path_to_html = f'{local_path_to_page}.html'
    path_to_html = os.path.join(dir, path_to_html)
    domain = get_domain(url)

    dir_name, dir_path = create_dir(dir, local_path_to_page)

    soup = BeautifulSoup(page_data.text, 'html.parser')
    elements = {}
    for key, value in TAGS.items():
        url = soup.find_all(key, {value: True})
        if value not in elements:
            elements.setdefault(value, url)
        else:
            elements[value].extend(url)

    assets = []
    for atribut, element in elements.items():
        for source in element:
            source_url = source[atribut]
            domain_lnk = get_domain(source_url)
            if domain_lnk == domain or domain_lnk == '://':
                source_url = ''.join(urlparse(source_url)[2:])
                source_url = domain + source_url
                local_file_path = to_file(source_url)
                full_path_to_file = os.path.join(dir_path, local_file_path)
                assets.append((source_url, full_path_to_file))
                source[atribut] = os.path.join(dir_name, local_file_path)
    html_data = soup.prettify()
    return html_data, assets, path_to_html
