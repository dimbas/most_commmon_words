import ast
import typing as t
from pathlib import Path

from nltk import pos_tag, word_tokenize

from .utils import flat, get_all_files


def is_magic_name(name: str) -> bool:
    return name.startswith('__') and name.endswith('__')


def is_function(node: ast.AST):
    return isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))


def is_assign(node: ast.AST):
    return isinstance(node, ast.Assign)


def get_trees(path: Path) -> t.Iterator[ast.AST]:
    for file in get_all_files(path, '.py'):
        content = file.read_text()
        try:
            tree = ast.parse(content)
        except SyntaxError:
            pass
        else:
            yield tree


def get_functions_from_path(path: Path) -> t.Iterable[ast.AST]:
    trees = get_trees(path)
    return (node for tree in trees
            for node in ast.walk(tree) if is_function(node) and not is_magic_name(node.name))


def get_variables_from_path(path: Path) -> t.Iterable[ast.AST]:
    def unfold_tuple(node: ast.Tuple):
        return node.elts

    trees = get_trees(path)
    assigns = (node.targets[0] for tree in trees
               for node in ast.walk(tree) if is_assign(node))

    return flat(unfold_tuple(node) if isinstance(node, ast.Tuple) else node
                for node in assigns)


def tokenize_names(words: str):
    # check if name is snake case or CamelCase
    return pos_tag(word_tokenize(words.replace('_', ' ')))
