# coding=utf-8
import ast
import typing as t
from pathlib import Path
from collections import Counter

from nltk import pos_tag
from nltk.downloader import Downloader

__version__ = '0.0.4-rc.1'


def flat(source: t.Iterable) -> list:
    """
    >>> flat([(1,2), (3,4)])
    ... [1, 2, 3, 4]
    """
    ret = []
    for item in source:
        if isinstance(item, list):
            ret.extend(item)
        else:
            ret.append(item)
    return ret


def is_verb(word: str) -> bool:
    if not word:
        return False
    pos_info = pos_tag([word])
    return pos_info[0][1].startswith('VB')


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


def get_verbs_from_function_name(function_name):
    return [word for word in function_name.split('_') if is_verb(word)]


def get_all_verbs_in_path(path: Path) -> t.Iterator[str]:
    def is_magic_name(name):
        return name.startswith('__') and name.endswith('__')

    def is_function(node):
        return isinstance(node, ast.FunctionDef) and not is_magic_name(node.name)

    trees = get_trees(path)
    functions = (node for tree in trees for node in ast.walk(tree) if is_function(node))

    return flat(get_verbs_from_function_name(func.name) for func in functions)


def most_common_verbs(paths: list, count: int) -> t.List[t.Tuple]:
    nltk_downloader = Downloader()
    if not nltk_downloader.is_installed('all'):
        nltk_downloader.download('all')

    words = flat(get_all_verbs_in_path(Path(p)) for p in paths)
    counter = Counter(words)

    return counter.most_common(count)


def show_most_common_verbs(paths: list, count: int):
    commons = most_common_verbs(paths, count)
    for word, quantity in commons:
        print(word, quantity)
