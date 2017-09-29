# coding=utf-8
import sys
import argparse
from pathlib import Path

from most_common_words import MostCommonWords, NLTKDownloader, NLTKDownloaderError, Printer


def parseargs(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', default='.', type=Path, help='Path to project. Default current folder.')
    parser.add_argument('-c', '--count', default=2, type=int,
                        help='Determines minimum number of occurrences words. Default 2.')
    parser.add_argument('-s', '--speech-part', choices=['verbs', 'nouns'], default='verbs',
                        help='Choose what part of speech to search. Default verbs.')
    parser.add_argument('-f', '--format', choices=['json', 'csv', 'humanable'], default='humanable',
                        help='Chose output format. Default humanable.')
    parser.add_argument('--pretty', action='store_true', help='Prettify output')

    return parser.parse_args(args)


def main(config):
    processor = MostCommonWords(config)
    downloader = NLTKDownloader()
    printer = Printer(config)

    try:
        downloader.check_installation()
    except NLTKDownloaderError as err:
        print('Cant check or download nltk data because of error {}'.format(err))
        return err.code
    except Exception as err:
        print('Cant check or download nltk data because of error {}'.format(err))
        return -1

    words = processor.get_words()
    printer.print(words)


def cli():
    args = parseargs()
    config = vars(args)

    sys.exit(main(config))
