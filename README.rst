=================
Most common words
=================


The utility for determining the most used words in python source code

* Free software: MIT
* Requirements

 * Python>=3.5.3
 * `nltk==3.2.4 <https://pypi.python.org/pypi/nltk>`_


--------
Features
--------

Finds most used verbs or nouns in python project

-----
Usage
-----

As command line util

.. code-block:: bash

    $ python -m most_common_words -p path/to/your/project -c minimum_count -s verbs

or

.. code-block:: bash

    $ most_common_words -p path/to/your/project -c minimum_count -s verbs

As library

.. code-block:: python

    import most_common_words as mcw
    config = {'path': '/your/path/to/project', 'count': any_count, 'speech_part': 'verbs or nouns'}
    processor = mcw.MostCommonWords(config)
    mcw.check_nltk_data_installation(yes=True)  # if you don`t know if data installed or not. it will installed automatically
    words = processor.get_words()

You can print returned words through builtin print. Example:

.. code-block:: python

    for word, times in words:
        print(word, times)

Or through ``Printer`` instance:

.. code-block:: python

    printer = mcw.Printer(config)
    printer.print(words)

Note: printer config requires `format` and `pretty` keys. `Format` on of 3 supported output formats (csv, json, humanable) and `pretty` if output must be prettified if it can be done.

Util needs nltk data to be downloaded, so if it is not installed script will ack you to download it (it may take tome time).

You can use ``check_installation()`` method call of NLTKDownloader instance to check and download nltk data. It gets 2 optional boolean arguments: ``yes`` and ``force_download``.
Or you can use raw nltk methods:

.. code-block:: python

    from nltk.downloader import Downloader
    downloader = Downloader()
    if not downloader.is_installed('all'):
        downloader.download('all')

-------
Options
-------

Run ``most_common_words --help`` for a full list of options and their effects.

.. code-block:: bash

    $ most_common_words --help
    usage: most_common_words [-h] [-p PATH] [-c COUNT] [-s {verbs,nouns}]
                             [-f {json,csv,humanable}] [--pretty]
                             [--skip-data-check]
                             [--console {stdout,stderr} | -o OUTPUT]

    optional arguments:
      -h, --help            show this help message and exit
      -p PATH, --path PATH  Path to project. Default current folder.
      -c COUNT, --count COUNT
                            Determines minimum number of occurrences words.
                            Default 2.
      -s {verbs,nouns}, --speech-part {verbs,nouns}
                            Choose what part of speech to search. Default verbs.
      -f {json,csv,humanable}, --format {json,csv,humanable}
                            Chose output format. Default humanable.
      --pretty              Prettify output
      --skip-data-check     Skips nltk data installation
      --console {stdout,stderr}
                            Prints returned data to stdout or stderr
      -o OUTPUT, --output OUTPUT
                            Prints returned data to file. (Overrides existing
                            file!)


---
API
---

module ``most_common_words.mcw``
================================

class ``most_common_words.mcw.MostCommonWords``
-----------------------------------------------

Main class

:attr: ``config``

    Holds base configuration.

:method: ``get_words() -> Iterable[tuple[word, count]]``

    Main function (aka entry point). Returns list of tuples there first element is word, second - count.


module ``most_common_words.utils``
==================================

Contains some helper functions

:function: ``flat(source: list) -> list``

    Unfolds received list of list and returns result. Not recursive, only 1 depth.

:function: ``is_magic_name(name: str) -> bool``

    Checks, is name is magic (starts and ends with double-underline symbols) or not.

:function: ``is_function(node: ast.AST) -> bool``

    Checks, if given ast node if function or not.

:function: ``tokenize_names(word: str) -> list[tuple[word, tag]]``

    Gets name, tokenize it and returns list of words, with nltk speech part tag.


module ``most_common_words.paths``
==================================

Contains functions to work with os folders, to parse source code and build ast

:function: ``get_all_files(path: pathlib.Path) -> Iterator[pathlib.Path]``

    Generator, walks through folders recursively and yields all files, wrapped in pathlib.Path.

:function: ``get_trees(path: pathlib.Path) -> Iterator[ast.AST]``

    Generator, yields ast from each file in path arg (calls ``get_all_files`` inside)

:function: ``get_functions_from_path(path: pathlib.Path) -> Iterable[ast.AST]``

    Generator, yields function nodes from all ast (calls ``get_trees`` inside)


module ``most_common_words.nltk_downloader``
============================================

Contains class encapsulates nltk data download logic and exceptions

:function: ``check_nltk_data_installation(yes=False: bool, force_download=False: bool)`` -> [int, None]

    Checks, if nltk data is installed. If it doesnt installed, asks permission to install in interactive mode and tries to download and install if permitted.
    If argument ``yes`` equals ``True``, than don't ask the permission and starts installation immediately. If argument ``force_download`` equals ``True``, than don't check installation and starts installation.
    In case of success it returns ``None``, otherwise returns error code.


class ``most_common_words.nltk_downloader.NLTKDownloader``
----------------------------------------------------------

Encapsulates download logic.

:attr: ``data_id``

    Nltk data id. By default ``'all'``

:method: ``check_installation(yes: bool, force_download: bool)``

    Checks, if nltk data is installed (by id from data_id). If it doesnt installed, asks permission to install in interactive mode and tries to download and install if permitted.
    If argument ``yes`` equals ``True``, than don't ask the permission and starts installation immediately. If argument ``force_download`` equals ``True``, than don't check installation and starts installation.

:method: ``_aks(yes: bool) -> str``

    If argument ``yes`` is ``False``, than asks user in interactive mode, start installation or not. Waits for `yes` or `no` only.
    If argument ``yes`` is ``True``, than don't start interactive session and returns.


class ``most_common_words.nltk_downloader.NLTKDownloaderError``
---------------------------------------------------------------

Base downloader exception.

class ``most_common_words.nltk_downloader.DownloadError``
---------------------------------------------------------

Error class, throws if data not installed and user rejected it. Inherits from ``most_common_words.nltk_downloader.NLTKDownloaderError``

class ``most_common_words.nltk_downloader.InternetError``
---------------------------------------------------------

Error class, throws if something throng with Internet connection. Installation check even needs internet. Inherits from ``most_common_words.nltk_downloader.NLTKDownloaderError``


module ``most_common_words.printer``
====================================

Contains output logic

class ``most_common_words.printer.Printer``
-------------------------------------------

Encapsulates printer logic.

:attr: ``config``

    Holds base configuration.

:property: ``formatter``

    Returns formatter class according on config

:property: ``writer``

    Returns configured Writer instance for current pointer. If searches config for key `writer`, if it presents return it. Otherwise it looks for `output` key, if its not ``None`` than return FileWriter targeting on file from config['output'] value.
    Otherwise it looks on `console``s key value and returns responding Writer (StdoutWriter or StdoutWriter).

:method: ``print(data: Iterable[tuple[word, count]])``

    Formats message from data and prints it.


package ``most_common_words.formatter``
=======================================

Package contains different formatter's implementations

class ``most_common_words.formatter.base.Formatter``
----------------------------------------------------

Abstract base class for any new formatter.

:absractmethod: ``format(data: Iterable[tuple[word, count]]) -> str``

    Main abstract method. Eny realization must receive data and return string.

class ``most_common_words.formatter.csv.CsvFormatter``
------------------------------------------------------

Implements abc ``most_common_words.formatter.base.Formatter``. Output is CSV.

class ``most_common_words.formatter.json.JsonFormatter``
--------------------------------------------------------

Implements abc ``most_common_words.formatter.base.Formatter``. Output is JSON.

class ``most_common_words.formatter.humanable.HumanableFormatter``
------------------------------------------------------------------

Implements abc ``most_common_words.formatter.base.Formatter``. Used as default, for humans.


module ``most_common_words.writer``
====================================

Contains classes, responsible for writing data for different places. All classes have only one method: ``write(data: str)``, which writes data.

class ``most_common_words.writer.FileWriter``
---------------------------------------------

Writes data to file. Constructor accepts file as ``pathlib.Path`` instance. Overrides existing file!

class ``most_common_words.writer.StdoutWriter``
-----------------------------------------------

Writes data to stdout.

class ``most_common_words.writer.StderrWriter``
-----------------------------------------------

Writes data to stderr.
