# coding=utf-8
import ast
import typing as t
from pathlib import Path
from collections import Counter
from urllib.error import URLError

from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.downloader import Downloader

__version__ = '0.0.6'


def flat(source: t.Iterable) -> list:
    """
    >>> flat([(1,2), (3,4)])
    ... [1, 2, 3, 4]
    >>> flat([[1,2], [[3,4],5]])
    ... [1, 2, [3, 4], 5]
    """
    ret = []
    for item in source:
        if isinstance(item, list):
            ret.extend(item)
        else:
            ret.append(item)
    return ret


def get_all_files(path: Path) -> t.Iterator[Path]:
    for item in path.iterdir():
        if item.is_dir():
            yield from get_all_files(item)
        elif item.is_file() and item.name.endswith('.py'):
            yield item


def get_trees(path: Path) -> t.Iterator[ast.AST]:
    for file in get_all_files(path):
        content = file.read_text()
        try:
            tree = ast.parse(content)
        except SyntaxError:
            pass
        else:
            yield tree


def is_magic_name(name: str) -> bool:
    return name.startswith('__') and name.endswith('__')


def is_function(node):
    return isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))


def tokenize_names(words: str):
    # check if name is snake case or CamelCase
    return pos_tag(word_tokenize(words.replace('_', ' ')))


def get_functions_from_path(path: Path) -> t.Iterable[ast.AST]:
    trees = get_trees(path)
    return (node for tree in trees
            for node in ast.walk(tree) if is_function(node) and not is_magic_name(node.name))


class MostCommonWords:
    def __init__(self, config):
        self.config = config

        if self.speech_part == 'verbs':
            self.get_words = self._most_common_verbs
        elif self.speech_part == 'nouns':
            self.get_words = self._most_common_nouns

        self.nltk_downloader = Downloader()

    @property
    def path(self):
        return self.config['path']

    @property
    def speech_part(self):
        return self.config['speech_part']

    @property
    def count(self):
        return self.config['count']

    def _get_names(self) -> t.Iterable[str]:
        return (func.name for func in get_functions_from_path(self.path))

    def _most_common_verbs(self) -> t.Iterable[t.Tuple]:
        return filter(lambda x: x[1] >= self.count, Counter(self._get_all_verbs()).most_common())

    def _get_all_verbs(self) -> t.Iterable[str]:
        words_n_tags = flat(tokenize_names(x) for x in self._get_names())
        return (word for word, tag in words_n_tags if tag.startswith('VB'))

    def _most_common_nouns(self) -> t.Iterable[t.Tuple]:
        return filter(lambda x: x[1] >= self.count, Counter(self._get_all_nouns()).most_common())

    def _get_all_nouns(self) -> t.Iterable[str]:
        words_n_tags = flat(tokenize_names(x) for x in self._get_names())
        return (word for word, tag in words_n_tags if tag.startswith('NN'))

    def download_nltk_data(self, yes=False, force_download=False):
        """
        :param yes: if True, it wont ask to install data (default False)
        :param force_download: if True, install data anyway (default False)
        """
        class InternetError(URLError):
            code = 1

        class DownloadError(ImportError):
            code = 2

        def question(yes):
            if yes:
                return 'yes'

            answer = input('For work you need installed nltk data, do you want to install it? [yes?no]: ').lower()
            while answer not in ('yes', 'no'):
                answer = input('Type yes or no: ').lower()
            return answer

        try:
            is_installed = self.nltk_downloader.is_installed('all')
        except URLError as err:
            print('You need internet connection to check and download nltk data installation. Aborting!')
            raise InternetError(err.reason) from err

        if force_download:
            self.nltk_downloader.download('all')
            return

        if is_installed:
            return

        action = question(yes)
        if action == 'yes':
            print('Warning, installing may take some time')
            self.nltk_downloader.download('all')
        else:
            print('Script cant work without nltk data installed. Aborting!')
            raise DownloadError
