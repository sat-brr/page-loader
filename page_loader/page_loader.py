import requests
import os
import re


def get_page(link):
    page = requests.get(link)
    return page.text


def write_data(path, data):
    with open(path, 'w') as file:
        file.write(data)


def format_path_to_file(path, link):
    link = os.path.splitext(link)
    new_link = link[0]
    split_link = re.split(r'\W+', new_link)
    if split_link[0] == 'https' or split_link[0] == 'http':
        split_link.pop(0)
    file_name = '-'.join(split_link)
    if link[1] != '':
        file_name += link[1]
    else:
        file_name += '.html'
    full_path = f'{path}/{file_name}'
    return full_path


def download(path, link):
    data = get_page(link)
    full_path = format_path_to_file(path, link)
    write_data(full_path, data)
    return full_path
