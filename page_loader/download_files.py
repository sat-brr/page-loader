import requests
from progress.bar import Bar
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from page_loader.scripts.page_load import logger
from page_loader.work_with_paths import make_dir, make_path


TAGS = ('img', 'link', 'script')


def find_by_tag(parse):
    result = []
    for tag in TAGS:
        if tag == 'link':
            found = parse.find_all(tag, href=True)
            result.extend(found)
            continue
        found = parse.find_all(tag, src=True)
        result.extend(found)
    return result


def get_element_url(elem):
    try:
        elem_url = elem['src']
        return elem_url, 'src'
    except KeyError:
        elem_url = elem['href']
        return elem_url, 'href'


def get_domain(url):
    parse = urlparse(url)
    scheme = parse[0] + '://'
    host = parse[1]
    return scheme + host


def get_files(page, url, dir):
    new_dir, full_path = make_dir(dir, url)
    logger.info('Download files...')
    domain = get_domain(url)
    open_page = open(page)
    soup = BeautifulSoup(open_page, 'html.parser')
    elements = find_by_tag(soup)
    bar = Bar('Downloading:', max=len(elements))
    for element in elements:
        elem_url, key = get_element_url(element)
        domain_lnk = get_domain(elem_url)
        if domain_lnk == domain or domain_lnk == '://':
            elem_url = ''.join(urlparse(elem_url)[2:])
        full_url = domain + elem_url
        local_path_file = make_path(full_url, file=True)
        full_path_to_file = f'{full_path}/{local_path_file}'
        try:
            data = requests.get(full_url).content
            with open(full_path_to_file, 'wb') as file:
                file.write(data)
        except Exception:
            logger.warning(f'Download file ({full_url}) fail !!!')
        bar.next()
        element[key] = f"{new_dir}/{local_path_file}"
    saved_changes = soup.prettify()
    open_page.close()
    bar.finish()
    logger.info('Downloading files successful!')
    return saved_changes
