import logging
import sys


def install_logger():
    logger = logging.getLogger('page-loader')
    logger.setLevel(logging.DEBUG)
    f = logging.Formatter("%(levelname)s | %(name)s | %(message)s")
    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.INFO)
    sh.setFormatter(f)
    logger.addHandler(sh)
    return logger
