from genericpath import exists
import os
import requests_mock
import tempfile
from page_loader import page_loader
import pytest

TEST_LINK = 'https://text.ru/testing/txt.html'
MAIN_DIR = os.getcwd()
FIX_RES = 'text-ru-testing-txt.html'


def test_make_name():
    assert page_loader.make_path('http://www.gov.uk/') == \
        'www-gov-uk'
    assert page_loader.make_path('https://www.gov.uk/courses') == \
        'www-gov-uk-courses'
    assert page_loader.make_path('http://www.gov.uk/pictures.png',
                                 file=True) == \
        'www-gov-uk-pictures.png'
    assert page_loader.make_path('http://www.gov.uk/folder', dir=True) == \
        'www-gov-uk-folder_files'


def test_download_pics():
    with requests_mock.Mocker() as m:
        test_page = open('tests/fixtures/test_page.html', 'r').read()
        m.get('https://testing.ru/', text=test_page)
        pic1 = open('tests/fixtures/pic1.png', 'rb').read()
        m.get('https://testing.ru/tests/fixtures/pic1.png', content=pic1)
        pic2 = open('tests/fixtures/pic2.jpg', 'rb').read()
        m.get('https://testing.ru/tests/fixtures/pic2.jpg', content=pic2)
        pic3 = open('tests/fixtures/pics/pic3.png', 'rb').read()
        m.get('https://testing.ru/tests/fixtures/pics/pic3.png', content=pic3)
        with tempfile.TemporaryDirectory() as tmp_dir:
            page_loader.download('https://testing.ru/', tmp_dir)
            new_dir = tmp_dir + '/testing-ru_files'
            html_file = tmp_dir + '/testing-ru.html'
            file1 = new_dir + '/testing-ru-tests-fixtures-pic1.png'
            file2 = new_dir + '/testing-ru-tests-fixtures-pic2.jpg'
            file3 = new_dir + '/testing-ru-tests-fixtures-pics-pic3.png'
            assert exists(html_file)
            assert exists(new_dir)
            assert exists(file1)
            assert exists(file2)
            assert exists(file3)


def test_download_lnk_scr():
    with requests_mock.Mocker()as m:
        test_page = open('tests/fixtures/test_scr_link.html', 'r').read()
        m.get('https://testing.ru', text=test_page)
        link1 = open('tests/fixtures/links/link1.css', 'rb').read()
        m.get('https://testing.ru/tests/fixtures/links/link1.css',
              content=link1)
        script1 = open('tests/fixtures/scripts/script1.js', 'rb').read()
        m.get('https://testing.ru/tests/fixtures/scripts/script1.js',
              content=script1)
        with tempfile.TemporaryDirectory() as tmp_dir:
            page_loader.download('https://testing.ru', tmp_dir)
            new_dir = tmp_dir + '/testing-ru_files'
            file1 = new_dir + '/testing-ru-tests-fixtures-links-link1.css'
            file2 = new_dir + '/testing-ru-tests-fixtures-scripts-script1.js'
            file3 = new_dir + '/hexlet-io-assets-menu.css'
            file4 = new_dir + '/hexlet-io-v3-scr.js'
            assert exists(file1)
            assert exists(file2)
            assert not exists(file3)
            assert not exists(file4)


def test_bad_response():
    with requests_mock.Mocker()as m:
        m.get('https://testing.ru/', status_code=404)
        m.get('https://testing.ru/', status_code=500)
        m.get('https://testing.ru/', status_code=502)
        m.get('https://testing.ru/', status_code=400)
        with tempfile.TemporaryDirectory() as tmp_dir:
            with pytest.raises(SystemExit):
                page_loader.download('https://testing.ru/', tmp_dir)
                page_loader.download('https://testing.ru/', tmp_dir)
                page_loader.download('https://testing.ru/', tmp_dir)
                page_loader.download('https://testing.ru/', tmp_dir)


def test_dir_errors():
    with requests_mock.Mocker()as m:
        m.get('https://testing.ru/', status_code=404)
        with tempfile.TemporaryDirectory() as tmp_dir:
            fake_dir = f'{tmp_dir}/123'
            file_path = f'{tmp_dir}/123.txt', 'w'
            open(f'{tmp_dir}/123.txt', 'w')
            locked = f'{tmp_dir}/locked'
            os.mkdir(locked)
            os.chmod(locked, 000)
            with pytest.raises(SystemExit):
                page_loader.download('https://testing.ru/', fake_dir)
                page_loader.download('https://testing.ru/', file_path)
                page_loader.download('https://testing.ru/', locked)
