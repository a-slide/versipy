#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

# Long description from README file
with open("README.md", "r") as fh:
    long_description = fh.read()

# Collect info in a dictionary for setup.py
setup(
    name="__name__",
    description="__description__",
    version="__version__",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="__url__",
    author="__author__",
    author_email="__author_email__",
    license="__licence__",
    python_requires="__minimal_python__",
    classifiers=["__classifiers_1__", "__classifiers_2__", "__classifiers_3__", "__classifiers_4__", "__classifiers_5__"],
    install_requires=["__dependency1__", "__dependency2__", "__dependency3__"],
    packages=["__name__"],
    package_dir={"__name__": "__name__"},
    package_data={"__name__": ["templates/*"]},
    entry_points={"console_scripts": ["__entry_point1__"]},
)
