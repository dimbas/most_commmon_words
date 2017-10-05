# coding=utf-8
import sys
import argparse
import tempfile
from pathlib import Path

from . import MostCommonWords, Printer, GitHubClient, check_nltk_data_installation


def parseargs(args=None):
    parser = argparse.ArgumentParser()

    sub_parser = parser.add_subparsers()

    local = sub_parser.add_parser('local')
    local.add_argument('-p', '--path', default='.', type=Path, help='Path to project. Default current folder.')
    local.set_defaults(local=True)

    github = sub_parser.add_parser('github')
    github.add_argument('project-name')
    github.add_argument('-u', '--user', help='Github project owner.')
    github.set_defaults(github=True)

    github.add_argument('-l', '--login', default=None, help='Your Github login.')
    github.add_argument('-s', '--secret', default=None, help='Your Github password.')
    github.add_argument('-t', '--token', default=None, help='Your Github OAuth token.')

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

    funcs_or_vars = parser.add_mutually_exclusive_group()
    funcs_or_vars.add_argument('--functions', action='store_true', help='Goes through function names')
    funcs_or_vars.add_argument('--variables', action='store_true', help='Goes through variable names')

    return parser.parse_args(args)


def main(config):
    try:
        if 'github' in config:
            project_archive = tempfile.NamedTemporaryFile(prefix='mcw_temp_archive')
            project_folder = tempfile.TemporaryDirectory(prefix='mcw_temp_folder')

            client = GitHubClient(config)
            client.find_project()
            client.download_project(project_archive)
            client.unzip_project(project_archive, project_folder.name)

            config['path'] = Path(project_folder.name)

        processor = MostCommonWords(config)
        printer = Printer(config)

        if not config['skip_data_check']:
            ret = check_nltk_data_installation()
            if ret is not None:
                return ret

        words = processor.get_words()
        printer.print(words)
    finally:
        project_archive.close()
        project_folder.cleanup()


def cli():
    args = parseargs()
    config = vars(args)

    sys.exit(main(config))
