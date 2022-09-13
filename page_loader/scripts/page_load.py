#!/usr/bin/env python3
import logging
from requests import exceptions as error
from page_loader import downloader
from page_loader.cli import parsing_args
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


def main():
    args = parsing_args()
    logger = install_logger()
    try:
        downloader.download(args.link, args.output)
    except (error.ConnectionError,
            error.HTTPError) as err:
        logger.debug(err)
        logger.error('Connection error. Details in logs.')
        sys.exit(1)
    except (error.InvalidSchema,
            error.MissingSchema) as err:
        logger.debug(err)
        logger.error('Missing schema. Details in logs.')
        sys.exit(1)
    except (PermissionError, FileNotFoundError) as err:
        logger.debug(err)
        logger.error('Directory does not exist or access denied.')
        sys.exit(1)
    except Exception as err:
        logger.debug(err)
        logger.error('Oops. Something went wrong.')
        sys.exit(1)


if __name__ == '__main__':
    main()
