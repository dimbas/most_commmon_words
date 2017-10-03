import ast
import typing as t
from pathlib import Path

from .utils import is_function, is_magic_name, is_assign, flat


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
