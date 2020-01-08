#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import codecs

from setuptools import setup, find_packages

cwd = os.path.abspath(os.path.dirname(__file__))

def read(filename):
    with codecs.open(os.path.join(cwd, filename), 'rb', 'utf-8') as h:
        return h.read()


metadata = read(os.path.join(cwd, 'ronkyuu', '__init__.py'))

def extract_metaitem(meta):
    # swiped from https://hynek.me 's attr package
    meta_match = re.search(r"""^__{meta}__\s+=\s+['\"]([^'\"]*)['\"]""".format(meta=meta),
                           metadata, re.MULTILINE)
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError('Unable to find __{meta}__ string.'.format(meta=meta))


if __name__ == '__main__':
    setup(
        name='ronkyuu',
        version=extract_metaitem('version'),
        description=extract_metaitem('description'),
        long_description=read('README.md'),
        long_description_content_type='text/markdown',
        author=extract_metaitem('author'),
        author_email=extract_metaitem('email'),
        maintainer=extract_metaitem('author'),
        maintainer_email=extract_metaitem('email'),
        url=extract_metaitem('url'),
        download_url=extract_metaitem('download_url'),
        license=extract_metaitem('license'),
        packages=find_packages(exclude=('tests', 'docs')),
        platforms=['Any'],
        install_requires=[
            'requests',
            'beautifulsoup4',
            'mf2py',
            'html5lib',
        ],
        setup_requires=[
            'setuptools>=41.0.1',
            'wheel>=0.33.4',
            'pytest-runner'
        ],
        tests_require=['pytest'],
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Operating System :: OS Independent',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.7',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ]
    )
