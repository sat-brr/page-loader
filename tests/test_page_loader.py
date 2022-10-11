from genericpath import exists
import os
import requests_mock
import tempfile
from page_loader import downloader
from page_loader.url import create_dir, to_file, generate_page_path
import pytest


TEST_URL = 'https://testing.ru/'
FIXTURES_PATH = os.path.abspath('tests/fixtures')
TEST_PAGE_PATH = os.path.join(FIXTURES_PATH, 'test_page.html')
ASSETS = {'pic1.png': "pictures/pic1.png",
          'pic2.jpg': 'pictures/pic2.jpg',
          'pics/pic3.png': 'pictures/pic3.png',
          'scripts/script1.js': 'v3/script1.js',
          'links/link1.css': 'assets/link1.css'}


@pytest.fixture()
def tmp_dir():
    tmpdir = tempfile.TemporaryDirectory()
    return tmpdir


@pytest.mark.parametrize('test_url, url_data',
                         [(TEST_URL,
                          open(TEST_PAGE_PATH, 'r').read())])
def test_downloader(test_url, url_data, tmp_dir):
    with requests_mock.Mocker() as mock:
        mock.get(test_url, text=url_data)
        for path, url in ASSETS.items():
            path = os.path.join(FIXTURES_PATH, path)
            with open(path, 'rb') as pic:
                tmp = pic.read()
            mock.get(f'{TEST_URL}{url}', content=tmp)
        html_file = downloader.download(TEST_URL, tmp_dir.name)

        path_url = generate_page_path(TEST_URL)
        files_dir = create_dir(tmp_dir.name, path_url)[1]
        for path, url in ASSETS.items():
            path = os.path.join(FIXTURES_PATH, path)
            path_file = to_file(url)
            local_path = f'{path_url}-{path_file}'
            full_path_to_file = os.path.join(files_dir, local_path)
            assert exists(full_path_to_file)
        assert exists(files_dir)
        assert exists(html_file)
        files = os.listdir(files_dir)
        assert len(files) == 5


@pytest.mark.parametrize("code", [400, 404, 500, 502])
def test_bad_response(code, tmp_dir):
    with requests_mock.Mocker()as mock:
        mock.get(TEST_URL, status_code=code)
        with pytest.raises(Exception):
            downloader.download(TEST_URL, tmp_dir.name)


def test_dir_errors(tmp_dir):
    with requests_mock.Mocker()as mock:
        mock.get(TEST_URL, text='404')
        fake_dir = os.path.join(tmp_dir.name, 'fake')
        file_path = os.path.join(tmp_dir.name, '123.txt')
        open(file_path, 'w')
        locked = os.path.join(tmp_dir.name, 'locked')
        os.mkdir(locked)
        os.chmod(locked, 0o000)
        paths = (locked, fake_dir, file_path)
        for path in paths:
            with pytest.raises(Exception):
                downloader.download(TEST_URL, path)
