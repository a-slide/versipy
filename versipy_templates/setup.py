#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

# Long description from README file
with open("README.md", "r") as fh:
    long_description = fh.read()

# Collect info in a dictionary for setup.py
setup(
    name="NAME",
    description="DESCRIPTION",
    version="VERSION",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="URL",
    author="AUTHOR",
    author_email="EMAIL",
    license="LICENSE",
    python_requires="MINIMAL_PYTHON",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    install_requires=["DEPENDENCY_1", "DEPENDENCY_2", "DEPENDENCY_3"],
    packages=["NAME"],
    entry_points={"console_scripts": ["ENTRY_POINT_1"]},
)
