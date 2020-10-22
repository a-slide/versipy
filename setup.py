#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

# Long description from README file
with open("README.md", "r") as fh:
    long_description = fh.read()

# Collect info in a dictionary for setup.py
setup(
    name = "versipy",
    description = "Simple python version managment in source code, git and across packaging ecosystem",
    version = "3.1.0.dev1",
    long_description = long_description,
    long_description_content_type="text/markdown",
    url = "https://github.com/a-slide/versipy",
    author = "Adrien Leger",
    author_email = "contact AT adrienleger DOT com",
    license = "MIT",
    python_requires = ">=3.6",
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'],
    install_requires = ['colorlog>=4.1.0', 'pyyaml>=5.3.1'],
    packages = [versipy],
    entry_points = {'console_scripts': ['versipy=versipy.__main__:main']})
