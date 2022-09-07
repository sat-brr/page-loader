#!/usr/bin/env python3
from page_loader.logger import install_logger
from page_loader import downloader
from page_loader.cli import parsing_args


logger = install_logger()


def main():
    args = parsing_args()
    try:
        downloader.download(args.link, args.output)
    except Exception as err:
        logger.debug(err)
        SystemExit(1)


if __name__ == '__main__':
    main()
