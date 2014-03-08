#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

# use requirements.txt for dependencies
with open('requirements.txt') as f:
    required = map(lambda s: s.strip(), f.readlines())

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='ronkyuu',
    version='0.1.0',
    description='Webmention Manager',
    long_description=readme,
    install_requires=required,
    author='Mike Taylor',
    author_email='bear@bear.im',
    url='https://github.com/bear/ronkyuu',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)