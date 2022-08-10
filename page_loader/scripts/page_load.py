#!/usr/bin/env python3
from page_loader.page_loader import download
from page_loader.cli import parsing_args


def main():
    args = parsing_args()
    print(download(args.output, args.link))


if __name__ == '__main__':
    main()
