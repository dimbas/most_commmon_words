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

Finds most used verbs or nouns in local or github python project.

-----
Usage
-----

As command line util

.. code-block:: bash

    $ most_common_words -c minimum_count -s verbs local -p path/to/your/project

or

.. code-block:: bash

    $ most_common_words -c minimum_count -s verbs github flask -u pallets

As library

.. code-block:: python

    import most_common_words as mcw
    config = {'path': '/your/path/to/project', 'count': any_count, 'speech_part': 'verbs or nouns'}
    processor = mcw.MostCommonWords(config)
    mcw.check_nltk_data_installation(yes=True)  # if you don`t know if data installed or not. it will installed automatically
    words = processor.get_words()

or with github project

.. code-block:: python

    from pathlib import Path
    import most_common_words as mcw
    config = {'project-name': 'project name', 'count': any_count, 'speech_part': 'verbs or nouns'}
    gh = mcw.Client(config)
    gh.find_project()
    gh.download_project(archive_file_dest_fd)
    gh.unzip_project(archive_file_dest_fd, project_folder_dest)
    config['path'] = Path(project_folder_dest)
    processor = mcw.MostCommonWords(config)
    words = processor.get_words()

For ``archive_file_dest_fd`` and ``project_folder_dest`` you can use respectively ``tempfile.NamedTemporaryFile`` (at least any file descriptor)
and ``tempfile.TemporaryDirectory`` (in this case you must call ``name`` property on its object).

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
                             [--functions | --variables]
                             {local,github} ...

    positional arguments:
      {local,github}

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
      --functions           Goes through function names
      --variables           Goes through variable names

    $ most_common_words local -h
    usage: most_common_words local [-h] [-p PATH]

    optional arguments:
      -h, --help            show this help message and exit
      -p PATH, --path PATH  Path to project. Default current folder.

    $ most_common_words github -h
    usage: most_common_words github [-h] [-u USER] [-l LOGIN] [-s SECRET]
                                    [-t TOKEN]
                                    project-name

    positional arguments:
      project-name

    optional arguments:
      -h, --help            show this help message and exit
      -u USER, --user USER  Github project owner.
      -l LOGIN, --login LOGIN
                            Your Github login.
      -s SECRET, --secret SECRET
                            Your Github password.
      -t TOKEN, --token TOKEN
                            Your Github OAuth token.


NOTE!

Any common arguments must be gone BEFORE `github` or `local` subcommands!

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
    Must have:

        - `path`: ``pathlib.Path`` instance
        - `speech_part`: `nouns` or `verbs`, str
        - `count`: minimum number of occurrences words, int
        - `variables`: go through variables in project, bool (excludes `functions` key)
        - `functions`: go through functions in project, bool (excludes `variables` key)

:method: ``get_words() -> Iterable[tuple[word, count]]``

    Main function (aka entry point). Returns list of tuples there first element is word, second - count.


module ``most_common_words.utils``
==================================

Contains some helper functions

:function: ``flat(source: t.Iterable) -> t.Iterable``

    Generator, yields item's content if its iterable (list, tuple, generator), otherwise yields item itself. Non recursive.

:function: ``get_all_files(path: pathlib.Path, extension: str) -> Iterator[pathlib.Path]``

    Generator, walks through folders recursively and yields all files with extension `extension`, wrapped in pathlib.Path.

module ``most_common_words.py_parser``
==================================

Contains functions to parse python source code.

:function: ``is_magic_name(name: str) -> bool``

    Checks, if name is magic (starts and ends with double-underline symbols) or not.

:function: ``is_function(node: ast.AST) -> bool``

    Checks, if given ast node is function or not.

:function: ``is_assign(node: ast.AST) -> bool``

    Checks, if given ast node is assign or not.

:function: ``tokenize_names(word: str) -> list[tuple[word, tag]]``

    Gets name, tokenize it and returns list of words, with nltk speech part tag.

:function: ``get_trees(path: pathlib.Path) -> Iterator[ast.AST]``

    Generator, yields ast from each file in path arg (calls ``get_all_files`` inside)

:function: ``get_functions_from_path(path: pathlib.Path) -> Iterable[ast.AST]``

    Generator, yields function nodes from all ast (calls ``get_trees`` inside)

:function: ``get_variables_from_path(path: pathlib.Path) -> Iterable[ast.AST]``

    Generator, yields assign's nodes targets from all ast (calls ``get_trees`` inside)

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
    Must have:
        - `format`: one of `csv`, `json` or `humanable`
        - `writer`: configured instance of any class from ``most_common_words.writer`` module (optional, excludes `output` and `console` keys)
        - `output`: ``pathlib.Path`` instance (excludes `console` key)
        - `console`: one of `stdout` or `stderr` (excludes `output` key)

:property: ``formatter``

    Returns formatter class according on config

:property: ``writer``

    Returns configured Writer instance for current pointer. If searches config for key `writer`, if it presents return it. Otherwise it looks for `output` key, if its not ``None`` than return FileWriter targeting on file from config['output'] value.
    Otherwise it looks on `console`'s key value and returns responding Writer (StdoutWriter or StdoutWriter).

:method: ``print(data: Iterable[tuple[word, count]])``

    Formats message from data and prints it.


package ``most_common_words.formatter``
=======================================

Package contains different formatter's implementations

class ``most_common_words.formatter.base.Formatter``
----------------------------------------------------

Abstract base class for any new formatter.

:attr: ``config``

    Holds base configuration.
    Must have:
        - `pretty`: prettify output or not, bool
        - `speech_part`: `nouns` or `verbs`, str

:property: ``is_pretty``

    Returns `pretty` key from config.

:property: ``speech_part``

    Returns `speech_part` key from config.

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

:property: ``path``

    Returns `path` key from config.

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

module ``most_common_words.client``
===================================

Contains functionality  for interaction this GitHub API

class ``most_common_words.client.GitHubClient``
-----------------------------------------------

Class for interaction this GitHub API

:attr: ``config``

    Holds base configuration.
    Must have:
        - `project-name`: github project you want to search
        - all necessary keys for Printer: will used to create separate printer instance

    Optional keys:
        - `user`: github project owner. If presents, than finds exact project using name and owner.
        - `login`: your github login.
        - `secret`: your github password
        - `token`: your github OAuth token

:attr: ``found_project``

    Holds reference to found github project.

:attr: ``printer``

    Separate printer for client, to interact with user.

:property: ``project_name``

    Returns `project-name` key from config.

:proprety: ``project_owner``

    Returns `user` key from config.

:property: ``login``

    Returns `login` key from config.

:property: ``secret``

    Returns `secret` key from config.

:property: ``token``

    Returns `token` key from config.

:method: ``find_project()``

    Finds github project, according on ``project_name`` property and, if presents, ``project_owner`` property. If cant find project without ``project_owner`` start interactive session, there user choose right project or interrupts session.
    Found project writes to ``found_project`` attribute.

:method: ``download_project(archive_fd: FileDescriptor)``

    Downloads project zip archive and writes to file descriptor `archive_fd`.

:method: ``unzip_project(archive_fd: FileDescriptor, project_folder: str)``

    Unpacks project archive, writen to file descriptor `archive_fd` to `project_folder`
