import typing as t
from collections import Counter

from nltk.downloader import Downloader

from .paths import get_functions_from_path
from .utils import flat, tokenize_names


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
