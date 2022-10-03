from bs4 import BeautifulSoup
from urllib.parse import urlparse
from page_loader.url_handler import make_dir, make_path, get_domain
import os

TAGS = {'img': 'src', 'link': 'href', 'script': 'src'}


def find_by_tag(parse):
    result = {}
    for key, value in TAGS.items():
        url = parse.find_all(key, {value: True})
        if value not in result:
            result.setdefault(value, url)
        else:
            result[value].extend(url)
    return result


def prepare_html_data_and_content(data, url, dir):
    new_dir, full_path = make_dir(dir, url)
    domain = get_domain(url)
    soup = BeautifulSoup(data, 'html.parser')
    elements = find_by_tag(soup)
    urls_for_downloading = []
    for atribut, element in elements.items():
        for source in element:
            source_url = source[atribut]
            domain_lnk = get_domain(source_url)
            if domain_lnk == domain or domain_lnk == '://':
                source_url = ''.join(urlparse(source_url)[2:])
            else:
                continue
            source_url = domain + source_url
            local_path_file = make_path(source_url, file=True)
            full_path_to_file = os.path.join(full_path, local_path_file)
            urls_for_downloading.append((source_url, full_path_to_file))
            source[atribut] = os.path.join(new_dir, local_path_file)
    html_data = soup.prettify()
    return html_data, urls_for_downloading
