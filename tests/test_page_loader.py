from genericpath import exists
import os
import requests_mock
import tempfile
from page_loader import downloader
from page_loader.work_with_paths import make_path
import pytest


TEST_URL = 'https://testing.ru/'
FIXTURES_PATH = os.path.abspath('tests/fixtures')


def test_download_pics():
    with requests_mock.Mocker() as m:
        test_page = open(f'{FIXTURES_PATH}/test_page.html', 'r').read()
        m.get(TEST_URL, text=test_page)
        paths = ('tests/fixtures/pic1.png',
                 'tests/fixtures/pic2.jpg',
                 'tests/fixtures/pics/pic3.png')
        for path in paths:
            with open(path, 'rb') as pic:
                tmp = pic.read()
            m.get(f'{TEST_URL}{path}', content=tmp)
        with tempfile.TemporaryDirectory() as tmp_dir:
            html_file = downloader.download('https://testing.ru/', tmp_dir)
            local_path_url = make_path(TEST_URL, dir=True)
            new_dir = f'{tmp_dir}/{local_path_url}'
            for path in paths:
                path_url = make_path(TEST_URL)
                path_file = make_path(path, file=True)
                local_path = f'{path_url}-{path_file}'
                path_to_file = f'{new_dir}/{local_path}'
                with open(path, 'rb') as file:
                    expected = file.read()
                with open(path_to_file, 'rb') as file:
                    result = file.read()
                assert exists(path_to_file)
                assert result == expected
            assert exists(html_file)
            assert exists(new_dir)


def test_download_link_scripts():
    with requests_mock.Mocker()as m:
        test_page = open(f'{FIXTURES_PATH}/test_scr_link.html', 'r').read()
        m.get(TEST_URL, text=test_page)
        paths = ('tests/fixtures/links/link1.css',
                 'tests/fixtures/scripts/script1.js',)
        for path in paths:
            with open(path, 'rb') as file:
                tmp = file.read()
            m.get(f'{TEST_URL}{path}', content=tmp)
        with tempfile.TemporaryDirectory() as tmp_dir:
            downloader.download('https://testing.ru', tmp_dir)
            local_path_url = make_path(TEST_URL, dir=True)
            new_dir = f'{tmp_dir}/{local_path_url}'
            for path in paths:
                path_url = make_path(TEST_URL)
                path_file = make_path(path, file=True)
                local_path = f"{path_url}-{path_file}"
                path_to_file = f'{new_dir}/{local_path}'
                with open(path, 'rb') as file:
                    expected = file.read()
                with open(path_to_file, 'rb') as file:
                    result = file.read()
                assert exists(path_to_file)
                assert result == expected
            fake_file1 = new_dir + '/hexlet-io-assets-menu.css'
            fake_file2 = new_dir + '/hexlet-io-v3-scr.js'
            assert not exists(fake_file1)
            assert not exists(fake_file2)


def test_bad_response():
    with requests_mock.Mocker()as m:
        m.get('testing.ru/404', status_code=404)
        m.get('https://testing.ru/500', status_code=500)
        m.get('https://testing.ru/502', status_code=502)
        m.get('https://testing.ru/400', status_code=400)
        with tempfile.TemporaryDirectory() as tmp_dir:
            with pytest.raises(Exception):
                downloader.download('testing.ru/404', tmp_dir)
                downloader.download('https://testing.ru/500', tmp_dir)
                downloader.download('https://testing.ru/502', tmp_dir)
                downloader.download('https://testing.ru/400', tmp_dir)


def test_dir_errors():
    with requests_mock.Mocker()as m:
        m.get('https://testing.ru/', status_code=404)
        with tempfile.TemporaryDirectory() as tmp_dir:
            fake_dir = f'{tmp_dir}/123'
            file_path = f'{tmp_dir}/123.txt', 'w'
            open(f'{tmp_dir}/123.txt', 'w')
            locked = f'{tmp_dir}/locked'
            os.mkdir(locked)
            os.chmod(locked, 0o000)
            with pytest.raises(Exception):
                downloader.download('https://testing.ru/', locked)
                downloader.download('https://testing.ru/', fake_dir)
                downloader.download('https://testing.ru/', file_path)
