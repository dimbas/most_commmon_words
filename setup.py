# coding=utf-8
from setuptools import find_packages, setup

with open('most_common_words/__init__.py') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.strip().split('=')[1].strip(' \'"')
            break
    else:
        version = '0.0.1'

with open('README.rst', 'rb') as f:
    README = f.read().decode()

with open('requirements/common.txt') as fp:
    REQUIRES = [x.strip() for x in fp.readlines()]

with open('requirements/dev.txt') as fp:
    TEST_REQUIREMENTS = [x.strip() for x in fp.readlines() if not x.startswith('-r')]


setup(
    name='most_common_words',
    version=version,
    description='',
    long_description=README,
    author='Tambovcev D.A.',
    author_email='tambovcev.dmitry@yandex.ru',
    maintainer='Tambovcev D.A.',
    maintainer_email='tambovcev.dmitry@yandex.ru',
    url='https://github.com/dimbas/most_common_words',
    license='MIT',

    keywords=[
        '',
    ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
    ],

    install_requires=REQUIRES,
    tests_require=TEST_REQUIREMENTS,

    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'most_common_words = most_common_words.cli:cli',
        ],
    },
)
