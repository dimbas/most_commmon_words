=================
Most common words
=================


The utility for determining the most used words

* Free software: MIT
* Requirements

 * Python>=3.5.3
 * `nltk==3.2.4 <https://pypi.python.org/pypi/nltk>`_


Features
--------

Finds most used verbs or nouns in python project

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
    processor.download_nltk_data(yes=True) # if you don`t know if data installed or not. it will installed automatically
    words = processor.get_words()
    for word, quantity in words:
        print(word, quantity)


Util needs nltk data to be downloaded, so if it is not installed script will ack you to download it (it may take tome time).

You can use `download_nltk_data()` method call of MostCommonWords instance to check and download nltk data. It gets 2 optional boolean arguments: yes and force_download.
Or you can use raw nlyk methods:

.. code-block:: python

    from nltk.downloader import Downloader
    downloader = Downloader()
    if not downloader.is_installed('all'):
        downloader.download('all')
