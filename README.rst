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

Finds most used verbs in python source code directories

Usage
-----

As command line util

.. code-block:: bash

    $ python -m most_common_words -p path/to/your/source/code/dir1 path/to/your/source/code/dir2 -c minimum_count

or

.. code-block:: bash

    $ most_common_words -p path/to/your/source/code/dir1 path/to/your/source/code/dir2 -c minimum_count

As library

.. code-block:: python

    import most_common_words as mcw
    commons = mcw.most_common_verbs(['.', 'path/to/your/source/code/dir'], 10)
    for word, quantity in commons:
        print(word, quantity)


Util needs nltk data to be downloaded, so if it is not installed script will ack you to download it (it may take tome time).

You can use `download_data()` call to check and download nltk data. It gets 2 optional boolean arguments: yes and force_download.
