import logging
import sys


def install_logger():
    logger = logging.getLogger('page-loader')
    logger.setLevel(logging.INFO)
    f = logging.Formatter("%(levelname)s | %(name)s | %(message)s")
    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.INFO)
    sh.setFormatter(f)
    logger.addHandler(sh)
    fh = logging.FileHandler('logs.txt')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(f)
    logger.addHandler(fh)
