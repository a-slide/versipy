# __package_name__ v__package_version__

![](pictures/versipy.png)

[![GitHub license](https://img.shields.io/github/license/a-slide/versipy.svg)](https://github.com/a-slide/versipy/blob/master/LICENSE)
[![Language](https://img.shields.io/badge/Language-Python3.6+-yellow.svg)](https://www.python.org/)
[![Build Status](https://travis-ci.com/a-slide/versipy.svg?branch=master)](https://travis-ci.com/a-slide/versipy)
[![DOI](https://zenodo.org/badge/194113600.svg)](https://zenodo.org/badge/latestdoi/194113600)

[![PyPI version](https://badge.fury.io/py/versipy.svg)](https://badge.fury.io/py/versipy)
[![PyPI Downloads](https://pepy.tech/badge/versipy)](https://pepy.tech/project/versipy)
[![Anaconda Version](https://anaconda.org/aleg/versipy/badges/version.svg)](https://anaconda.org/aleg/versipy)
[![Anaconda Downloads](https://anaconda.org/aleg/versipy/badges/downloads.svg)](https://anaconda.org/aleg/versipy)

---

**__package_description__**

---

## Summary

`versipy` is a versatile tool to centrally manage the package metadata and its version following the
[PEP 440 version specification](https://www.python.org/dev/peps/pep-0440/).
`versipy` propagates metadata values from a YAML file to target files specified by the user such as the
`setup.py`, `__init__.py`, `meta.yaml` and `README` files. To do so it uses a simple string replacement strategy
using templates files defined by the user containing placeholder values. In addition, `versipy` is able to automatically
add, commit and push the modified files to a remote git repository and set a remote version tag.

![](pictures/python_version.png)


## Installation

Ideally, before installation, create a clean **python3.6+** virtual environment to deploy the package.
Earlier version of Python3 should also work but **Python 2 is not supported**.
For example with [conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html):

```bash
conda create -n versipy python=3.6
conda activate versipy
```

### Install or upgrade the package with pip from pypi

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

- __dependency1__
- __dependency2__
- __dependency3__

## Usage

Setting up your repository requires a bit of manual work but afterwards a single command can bump_up the version and
propagate it to several python packaging ecosystem files including the `setup.py`, `__init__.py`, `meta.yaml` and
`README` files. `versipy` can also optionally commit and push the changes to a remote git repository and set a git tag.

### Setting up your repository

* Open a terminal in the root directory of the (git managed) code repository you want to use with `versipy`

* Create a template versipy YAML file

```bash
versipy init_repo
```

You should now be able to see 2 new files: `versipy.yaml` which will contain all the repository metadata and
`versipy_history.txt` where `versipy` will keep a track of the version changes history.

#### The versipy.yaml file

[Example file](https://github.com/a-slide/versipy/blob/master/versipy.yaml)

* `version` section

This section contains individual numbers for each sections of the full version number. Although it can be manually
modified, this is supposed to be managed directly via the command line with the `set_version` and `bump_up_version`
subcommands.

* `managed_values` section

key:value fields corresponding to a placeholder key to be found in template managed files and the corresponding
replacement value that can be customized. Users can add as many extra entries and they wish. It is recommended to
define explicit descriptive keys and to use the python double underscore syntax to avoid replacing random words in the
code

* `managed_files` section

key:value fields corresponding to the path of a template file containing placeholder keys as defined in the previous
section and the corresponding destination path where to write a file containing the replacement values.   

### Bump up or set the version number

The version number can be easily incremented using `bump_up_version` according to the level selected by users following
the [PEP 440 version specification](https://www.python.org/dev/peps/pep-0440/) as defined above.
Several levels can be incremented at once, but lower levels are always reset to 0 (or discarded for a, b, rc, post and
dev). For example if incrementing the minor level, the micro is set to 0 and the alpha, beta, rc, post and dev levels
are discarded if they were previously set.

```bash
# Bumping up minor level version
versipy bump_up_version --minor

# Bumping up minor and setting the dev level to 1
versipy bump_up_version --minor --dev

# Bumping up post level + publish changes to a remote git branch
versipy bump_up_version --post --git_push

# Bumping up major version + publish changes to a remote git branch  + create a git tag and use a custom comment
versipy bump_up_version --major --git_push --git_tag --comment "Major version update"
```

If you want to jump to a different number, the required tag can be directly set by passing a specific value to
`set_version`. An error will be raised if the version is not canonical.

```bash
versipy set_version --version_str "1.23rc1.post2"
```

### Going further with continuous deployment

Used in combination with `on tag` continuous deployment, `versipy` provides a powerful toolset to greatly simplify
package building and distribution. Here is an example YAML code snippet for
[Travis CI](https://docs.travis-ci.com/user/deployment/) to auto-deploy a package upon tag publishing to PyPI, anaconda
cloud and set a create Release

```yaml

dist: xenial
language: python
python: 3.6

install: true

script: true

deploy:

  # Production version deployment
  - provider: pypi
    skip_cleanup: true
    user: aleg
    password: "$PYPI_PW"
    on:
      tags: true

  - provider: script
    skip_cleanup: true
    script: bash ./deploy_anaconda.sh $ANACONDA_TOKEN
    on:
      tags: true

  - provider: releases
    api_key: $GITHUB_TOKEN
    skip_cleanup: true
    on:
      tags: true
```

---

## Classifiers

* __classifiers_1__
* __classifiers_2__
* __classifiers_3__
* __classifiers_4__
* __classifiers_5__

## citation

__citation__

## licence

__package_licence__ (__package_licence_url__)

Copyright © 2020 __author_name__

## Authors

* __author_name__ / __author_email__ / __author_url__
