from genericpath import exists
import os
import requests_mock
import tempfile
from page_loader import page_loader


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
            page_loader.download(tmp_dir, 'https://testing.ru/')
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
