import typing as t
from pathlib import Path


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


def get_all_files(path: Path, extension: str) -> t.Iterator[Path]:
    for item in path.iterdir():
        if item.is_dir():
            yield from get_all_files(item, extension)
        elif item.is_file() and item.name.endswith(extension):
            yield item
