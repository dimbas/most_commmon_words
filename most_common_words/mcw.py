import ast
import typing as t
from collections import Counter

from .py_parser import get_functions_from_path, get_variables_from_path, tokenize_names
from .utils import flat


class MostCommonWords:
    def __init__(self, config):
        self.config = config

        if self.speech_part == 'verbs':
            self.get_words = self._most_common_verbs
        elif self.speech_part == 'nouns':
            self.get_words = self._most_common_nouns

        if self.config['variables']:
            self._get_names = self._get_variables_names
        else:
            self._get_names = self._get_functions_names

    @property
    def path(self):
        return self.config['path']

    @property
    def speech_part(self):
        return self.config['speech_part']

    @property
    def count(self):
        return self.config['count']

    def _get_functions_names(self) -> t.Iterable[str]:
        return (func.name for func in get_functions_from_path(self.path))

    def _get_variables_names(self) -> t.Iterable[str]:
        def _get_name(node: ast.AST):
            if isinstance(node, ast.Name):
                return node.id
            if isinstance(node, ast.Attribute):
                return node.attr

        return (_get_name(var) for var in get_variables_from_path(self.path))

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
