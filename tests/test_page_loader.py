from genericpath import exists
import os
import requests_mock
from page_loader import downloader
from page_loader.url import to_dir, to_file, generate_page_path
import pytest


TEST_URL = 'https://testing.ru/'
FIXTURES_PATH = os.path.abspath('tests/fixtures')
TEST_PAGE_PATH = os.path.join(FIXTURES_PATH, 'test_page.html')
ASSETS = {'pic1.png': "pictures/pic1.png",
          'pic2.jpg': 'pictures/pic2.jpg',
          'pics/pic3.png': 'pictures/pic3.png',
          'scripts/script1.js': 'v3/script1.js',
          'links/link1.css': 'assets/link1.css'}


@pytest.mark.parametrize('test_url, test_url_path',
                         [(TEST_URL,
                          TEST_PAGE_PATH)])
def test_downloader(test_url, test_url_path, tmpdir):
    with requests_mock.Mocker() as mock:
        test_url_data = open(test_url_path, 'r').read()
        mock.get(test_url, text=test_url_data)
        for path, url in ASSETS.items():
            path = os.path.join(FIXTURES_PATH, path)
            with open(path, 'rb') as pic:
                tmp = pic.read()
            mock.get(f'{TEST_URL}{url}', content=tmp)
        html_file = downloader.download(TEST_URL, tmpdir)

        path_url = generate_page_path(TEST_URL)
        files_dir = os.path.join(tmpdir, to_dir(TEST_URL))
        for path, url in ASSETS.items():
            path = os.path.join(FIXTURES_PATH, path)
            file_path = to_file(url)
            local_path = f'{path_url}-{file_path}'
            full_path_to_file = os.path.join(files_dir, local_path)
            assert exists(full_path_to_file)
        assert exists(files_dir)
        assert exists(html_file)
        files = os.listdir(files_dir)
        assert len(files) == 5


@pytest.mark.parametrize("code", [400, 404, 500, 502])
def test_bad_response(code, tmpdir):
    with requests_mock.Mocker()as mock:
        mock.get(TEST_URL, status_code=code)
        with pytest.raises(Exception):
            downloader.download(TEST_URL, tmpdir)


def test_dir_errors(tmpdir):
    with requests_mock.Mocker()as mock:
        mock.get(TEST_URL, text='404')
        fake_dir = os.path.join(tmpdir, 'fake')
        file_path = os.path.join(tmpdir, '123.txt')
        open(file_path, 'w')
        locked = os.path.join(tmpdir, 'locked')
        os.mkdir(locked)
        os.chmod(locked, 0o000)
        paths = (locked, fake_dir, file_path)
        for path in paths:
            with pytest.raises(Exception):
                downloader.download(TEST_URL, path)
