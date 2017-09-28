# coding=utf-8
import sys
import argparse
from pathlib import Path

from most_common_words import MostCommonWords


def parseargs(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', default='.', type=Path, help='path to project')
    parser.add_argument('-c', '--count', default=2, type=int, help='determines minimum number of occurrences words')
    parser.add_argument('-s', '--speech-part', choices=['verbs', 'nouns'], default='verbs',
                        help='choose what part of speech to search')

    return parser.parse_args(args)


def show_most_common_words(words, speech_part, path: Path):
    print('Most common {part} in path {path}'.format(part=speech_part, path=path.absolute()))
    for item in words:
        print('\t{word}: {times}'.format(word=item[0], times=item[1]))


def main(config):
    processor = MostCommonWords(config)

    try:
        processor.download_nltk_data()
    except Exception as err:
        print('Cant check or download nltk data because of error {}'.format(err))
        return err.code if hasattr(err, 'code') else -1

    words = processor.get_words()
    show_most_common_words(words, processor.speech_part, processor.path)


def cli():
    args = parseargs()
    config = vars(args)

    sys.exit(main(config))
