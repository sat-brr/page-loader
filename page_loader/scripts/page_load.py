#!/usr/bin/env python3
import logging
from page_loader import downloader
from page_loader.cli import parsing_args
import sys


FORMATTER = "%(levelname)s | %(name)s | %(message)s"


def main():
    args = parsing_args()
    logging.basicConfig(level=logging.INFO,
                        format=FORMATTER,
                        handlers=[logging.StreamHandler(), ])
    try:
        path_to_html = downloader.download(args.link, args.output)
        logging.info(f"Page was downloaded as '{path_to_html}'.")
    except Exception as err:
        logging.debug(err)
        logging.error('Oops. Something went wrong. See logs.')
        sys.exit(1)


if __name__ == '__main__':
    main()
