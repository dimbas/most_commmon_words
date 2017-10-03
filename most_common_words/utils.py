import ast
import typing as t

from nltk import pos_tag, word_tokenize


def flat(source: t.Iterable) -> t.Iterable:
    """
    >>> flat([(1,2), (3,4)])
    ... [1, 2, 3, 4]
    >>> flat([[1,2], [[3,4],5]])
    ... [1, 2, [3, 4], 5]
    """
    for item in source:
        if isinstance(item, (list, tuple, t.Generator)):
            yield from item
        else:
            yield item


def is_magic_name(name: str) -> bool:
    return name.startswith('__') and name.endswith('__')


def is_function(node: ast.AST):
    return isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))


def is_assign(node: ast.AST):
    return isinstance(node, ast.Assign)


def tokenize_names(words: str):
    # check if name is snake case or CamelCase
    return pos_tag(word_tokenize(words.replace('_', ' ')))
