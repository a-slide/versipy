# versipy v0.1.dev4

![versipy](pictures/versipy.png)

[![GitHub license](https://img.shields.io/github/license/a-slide/versipy.svg)](https://github.com/a-slide/versipy/blob/master/LICENSE)
[![Language](https://img.shields.io/badge/Language-Python3.6+-yellow.svg)](https://www.python.org/)
[![Build Status](https://travis-ci.com/a-slide/versipy.svg?branch=master)](https://travis-ci.com/a-slide/versipy)

[![PyPI version](https://badge.fury.io/py/versipy.svg)](https://badge.fury.io/py/versipy)
[![PyPI Downloads](https://pepy.tech/badge/versipy)](https://pepy.tech/project/versipy)
[![Anaconda Version](https://anaconda.org/aleg/versipy/badges/version.svg)](https://anaconda.org/aleg/versipy)
[![Anaconda Downloads](https://anaconda.org/aleg/versipy/badges/downloads.svg)](https://anaconda.org/aleg/versipy)

--

**Versatile version and medatada managment across the python packaging ecosystem, integrated with git**

--

## Installation


### Create a clean virtual environment (optional )

Ideally, before installation, create a clean **python3.6+** virtual environment to deploy the package.
Earlier version of Python3 should also work but **Python 2 is not supported**.
For example with [conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html):

```bash
conda create -n versipy python=3.6
conda activate versipy
```

### Install versipy

#### Install or upgrade the package with pip from pypi

```bash
# Install
pip install versipy

# Update
pip install versipy --update
```

### Install or upgrade the package with conda from Anacounda cloud

```bash
# Install
conda install -c aleg -c anaconda -c bioconda -c conda-forge versipy=[VERSION]

# Update
conda update -c aleg -c anaconda -c bioconda -c conda-forge versipy
```

### Dependencies

The following dependencies are required but automatically installed with pip or conda package manager

- colorlog>=4.1.0
- pyyaml>=5.3.1
- gitpython>=3.1.9

## Quick Start

* Open a terminal in the code repository you want to manage with versipy

* Create a template versipy YAML file
```bash
versipy init
```

* There is a bit of manual work to define templates for the files you want to manage and customize 

--

## Classifiers

* Development Status :: 3 - Alpha
* Intended Audience :: Science/Research
* Topic :: Scientific/Engineering :: Bio-Informatics
* License :: OSI Approved :: GNU General Public License v3 (GPLv3)
* Programming Language :: Python :: 3

## licence

GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)

Copyright © 2020 Adrien Leger

## Authors

* Adrien Leger / contact@adrienleger.com / https://adrienleger.com/
