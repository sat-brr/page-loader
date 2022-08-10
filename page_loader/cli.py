import argparse
import os


def parsing_args():
    parser = argparse.ArgumentParser(description="""Download
                                     page from link.""")
    parser.add_argument('-o', '--output', type=str, default=os.getcwd(),
                        help='set path to download')
    parser.add_argument('link', type=str)
    return parser.parse_args()
