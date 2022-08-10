import pytest
import os
import requests_mock
import requests
import tempfile
from page_loader import page_loader


TEST_LINK = 'https://text.ru/testing/txt.html'
MAIN_DIR = os.getcwd()
FIX_RES = 'text-ru-testing-txt.html'

def fake_request(link):
    with requests_mock.Mocker() as mock:
        mock.get(link, text = 'success')
        data = requests.get(link).text
    return data


def test_page_loader():
    with tempfile.TemporaryDirectory() as tmp_dir:
        name_dir = tmp_dir
        page_loader.get_page = fake_request
        res = f'{name_dir}/{FIX_RES}'
        test = page_loader.download(name_dir, TEST_LINK)
        assert test == res
        with open(res, 'r') as tmp_file:
            assert tmp_file.read() == 'success'
