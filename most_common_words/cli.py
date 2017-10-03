# coding=utf-8
import sys
import argparse
from pathlib import Path

from . import MostCommonWords, Printer, check_nltk_data_installation


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
    parser.add_argument('--skip-data-check', action='store_true', help='Skips nltk data installation')

    printer = parser.add_mutually_exclusive_group()
    printer.add_argument('--console', choices=['stdout', 'stderr'], default='stdout',
                         help='Prints returned data to stdout or stderr')
    printer.add_argument('-o', '--output', type=Path, help='Prints returned data to file. (Overrides existing file!)')

    return parser.parse_args(args)


def main(config):
    processor = MostCommonWords(config)
    printer = Printer(config)

    if not config['skip_data_check']:
        ret = check_nltk_data_installation()
        if ret is not None:
            return ret

    words = processor.get_words()
    printer.print(words)


def cli():
    args = parseargs()
    config = vars(args)

    sys.exit(main(config))
