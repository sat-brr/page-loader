from genericpath import exists
import os
import requests_mock
import tempfile
from page_loader import downloader
from page_loader.url_handler import make_path
import pytest


TEST_URL = 'https://testing.ru/'
FIXTURES_PATH = os.path.abspath('tests/fixtures')
TEST_PAGE_PATH = os.path.join(FIXTURES_PATH, 'test_page.html')
ASSETS = {'pic1.png': "pictures/pic1.png",
          'pic2.jpg': 'pictures/pic2.jpg',
          'pics/pic3.png': 'pictures/pic3.png',
          'scripts/script1.js': 'v3/script1.js',
          'links/link1.css': 'assets/link1.css'}


@pytest.mark.parametrize('test_url, url_data',
                         [(TEST_URL,
                          open(TEST_PAGE_PATH, 'r').read())])
def test_downloader(test_url, url_data):
    with requests_mock.Mocker() as mock:
        mock.get(test_url, text=url_data)
        for path, url in ASSETS.items():
            path = os.path.join(FIXTURES_PATH, path)
            with open(path, 'rb') as pic:
                tmp = pic.read()
            mock.get(f'{TEST_URL}{url}', content=tmp)
        with tempfile.TemporaryDirectory() as tmp_dir:
            html_file = downloader.download(TEST_URL, tmp_dir)
            local_path_url = make_path(TEST_URL, dir=True)
            new_dir = os.path.join(tmp_dir, local_path_url)
            for path, url in ASSETS.items():
                path = os.path.join(FIXTURES_PATH, path)
                path_url = make_path(TEST_URL)
                path_file = make_path(url, file=True)
                local_path = f'{path_url}-{path_file}'
                path_to_file = os.path.join(new_dir, local_path)
                with open(path, 'rb') as file:
                    expected = file.read()
                with open(path_to_file, 'rb') as file:
                    result = file.read()
                assert exists(path_to_file)
                assert result == expected
            files = os.listdir(new_dir)
            assert len(files) == 5
            assert exists(html_file)
            assert exists(new_dir)


@pytest.mark.parametrize("code", [400, 404, 500, 502])
def test_bad_response(code):
    with requests_mock.Mocker()as mock:
        mock.get(TEST_URL, status_code=code)
        with tempfile.TemporaryDirectory() as tmp_dir:
            with pytest.raises(Exception):
                downloader.download(TEST_URL, tmp_dir)


def test_dir_errors():
    with requests_mock.Mocker()as mock:
        mock.get(TEST_URL, text='404')
        with tempfile.TemporaryDirectory() as tmp_dir:
            fake_dir = os.path.join(tmp_dir, '123')
            file_path = os.path.join(tmp_dir, '123.txt')
            open(file_path, 'w')
            locked = os.path.join(tmp_dir, 'locked')
            os.mkdir(locked)
            os.chmod(locked, 0o000)
            paths = (locked, fake_dir, file_path)
            for path in paths:
                with pytest.raises(Exception):
                    downloader.download(TEST_URL, path)
