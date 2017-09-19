# coding=utf-8
import sys
import argparse

from most_common_words import show_most_common_verbs


def parseargs(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--paths', default=['.'], nargs='*')
    parser.add_argument('-c', '--count', default=200, type=int)

    return parser.parse_args(args)


def cli():
    args = parseargs()
    sys.exit(show_most_common_verbs(paths=args.paths, count=args.count))
