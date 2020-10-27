#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

# Long description from README file
with open("README.md", "r") as fh:
    long_description = fh.read()

# Collect info in a dictionary for setup.py
setup(
    name="versipy",
    description="Versatile version and medatada managment across the python packaging with git integration ecosystem, integrated with git",
    version="0.2.3.dev2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/a-slide/versipy",
    author="Adrien Leger",
    author_email="contact@adrienleger.com",
    license="GPLv3",
    python_requires=">=3.6",
    classifiers=["Development Status :: 3 - Alpha", "Intended Audience :: Science/Research", "Topic :: Scientific/Engineering :: Bio-Informatics", "License :: OSI Approved :: GNU General Public License v3 (GPLv3)", "Programming Language :: Python :: 3"],
    install_requires=["colorlog>=4.1.0", "pyyaml>=5.3.1", "gitpython>=3.1.9"],
    packages=["versipy"],
    package_dir={"versipy": "versipy"},
    package_data={"versipy": ["templates/*"]},
    entry_points={"console_scripts": ["versipy=versipy.__main__:main"]},
)
