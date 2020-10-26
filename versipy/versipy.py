# -*- coding: utf-8 -*-

# IMPORTS ##############################################################################################################

# Standard library imports
import copy
from collections import OrderedDict
import datetime

# Third party imports

# Local imports
from versipy.common import *

# HEAD FUNCTIONS ################################################################################################


def init_repo(versipy_fn: str = "versipy.yaml", verbose: bool = False, quiet: bool = False, **kwargs):
    """
    * versipy_fn:
        Path to the versipy YAML info file
    """
    # Init method
    opt_summary_dict = opt_summary(local_opt=locals())
    log = get_logger(name="versipy init_repo", verbose=verbose, quiet=quiet)

    log.warning("Checking options and input files")
    log_dict(opt_summary_dict, log.debug, "Options summary")

    generate_versipy_yaml(versipy_fn=versipy_fn, log=log)

    # Create example templates ?


def current_version(versipy_fn: str = "versipy.yaml", verbose: bool = False, quiet: bool = False, **kwargs):
    """
    Return the current package version
    * versipy_fn:
        Path to the versipy YAML info file containing package metadata
    """
    # Init method
    opt_summary_dict = opt_summary(local_opt=locals())
    log = get_logger(name="versipy bump_up", verbose=verbose, quiet=quiet)
    log.warning("Bump up version package version")

    log.info("Checking options and input files")
    log_dict(opt_summary_dict, log.debug, "Options summary")

    # Load and check file
    info_d = get_versipy_yaml(versipy_fn=versipy_fn, log=log)
    version_str = get_version_str(info_d["version"])

    stdout_print(version_str)


def bump_up_version(
    major: bool = False,
    minor: bool = False,
    micro: bool = False,
    a: bool = False,
    b: bool = False,
    rc: bool = False,
    post: bool = False,
    dev: bool = False,
    versipy_fn: str = "versipy.yaml",
    versipy_history_fn: str = "versipy_history.txt",
    overwrite_all: bool = False,
    git_push: bool = False,
    message: str = "Versipy auto bump-up",
    verbose: bool = False,
    quiet: bool = False,
    **kwargs,
):
    """
    Increment the current package version number according to the level selected by users following the python PEP
    versionning definition. major#[.minor#][.micro#][a#|b#|rc#][.post#][.dev#]. Incrementing a level resets all the
    lower levels. Keeping this rule in mind, several levels can be incremented at once. Levels a, b, rc, post and dev
    are automatically removed if not used
    * major
        Increment the micro version level by 1
    * minor
        Increment the micro version level by 1
    * micro
        Increment the micro version level by 1
    * a
        Increment the alpha version level by 1
    * b
        Increment the beta version level by 1
    * rc
        Increment the release candidate version level by 1
    * post
        Increment the major post level by 1
    * dev
        Increment the major dev level by 1
    * versipy_fn:
        Path to the versipy YAML info file containing package metadata
    * versipy_history_fn
        Path to the versipy history file
    * overwrite_all
        Do not display a confirmation message before overwriting an existing file
    * git_push
        commit and push the files modified by versipy and set a git version tag
    * message
        Message used for the history file and the git commit is used in combination with `git_push`
    """
    # Init method
    opt_summary_dict = opt_summary(local_opt=locals())
    log = get_logger(name="versipy bump_up", verbose=verbose, quiet=quiet)
    log.warning("Bump up version package version")

    log.info("Checking options and input files")
    log_dict(opt_summary_dict, log.debug, "Options summary")

    # Load and check file
    info_d = get_versipy_yaml(versipy_fn=versipy_fn, log=log)
    previous_version_str = get_version_str(info_d["version"])

    log.info("Incrementing version number")
    info_d["version"] = increment_version(
        version_d=info_d["version"], major=major, minor=minor, micro=micro, a=a, b=b, rc=rc, post=post, dev=dev, log=log
    )
    version_str = get_version_str(info_d["version"])

    log.info("Update managed files")
    update_files(
        info_d=info_d,
        versipy_fn=versipy_fn,
        versipy_history_fn=versipy_history_fn,
        message=message,
        overwrite_all=overwrite_all,
        log=log,
    )

    # Optional git tagging
    if git_push:
        log.info(f"Attempting set tag and to push files to remote repository")
        managed_files = [f for f in info_d["managed_files"].values()]
        extra_files = [versipy_fn, versipy_history_fn]
        git_files(files=managed_files + extra_files, version=version_str, message=message, log=log)

    log.warning(f"Version updated: {previous_version_str} > {version_str}")


def set_version(
    version_str: str,
    versipy_fn: str = "versipy.yaml",
    versipy_history_fn: str = "versipy_history.txt",
    overwrite_all: bool = False,
    git_push: bool = False,
    message: str = "Manually set version",
    verbose: bool = False,
    quiet: bool = False,
    **kwargs,
):
    """
    Set the version from the provided version string. The version format need to follow python PEP versionning
    definition = major#[.minor#][.micro#][a#|b#|rc#][.post#][.dev#]. If not an error will be raised. The previous
    version is fully replaced.
    * version_str
        python PEP compliant version string (ex: 0.5, 1.2a1, 0.2.5.dev1, 1.2.4.rc1.post2)
    * versipy_fn:
        Path to the versipy YAML info file containing package metadata
    * versipy_history_fn
        Path to the versipy history file
    * overwrite_all
        Do not display a confirmation message before overwriting an existing file
    * git_push
        commit and push the files modified by versipy and set a git version tag
    * message
        Message used for the history file and the git commit is used in combination with `git_push`
    *
    """
    # Init method
    opt_summary_dict = opt_summary(local_opt=locals())
    log = get_logger(name="versipy bump_up", verbose=verbose, quiet=quiet)
    log.warning("Bump up version package version")

    log.info("Checking options and input files")
    log_dict(opt_summary_dict, log.debug, "Options summary")

    # Load and check file
    info_d = get_versipy_yaml(versipy_fn=versipy_fn, log=log)
    previous_version_str = get_version_str(info_d["version"])

    log.info("Set version number")
    info_d["version"] = parse_version_str(version_str=version_str, log=log)
    version_str = get_version_str(info_d["version"])

    log.info("Update managed files")
    update_files(
        info_d=info_d,
        versipy_fn=versipy_fn,
        versipy_history_fn=versipy_history_fn,
        message=message,
        overwrite_all=overwrite_all,
        log=log,
    )

    # Optional git tagging
    if git_push:
        log.info(f"Attempting set tag and to push files to remote repository")
        managed_files = [f for f in info_d["managed_files"].values()]
        extra_files = [versipy_fn, versipy_history_fn]
        git_files(files=managed_files + extra_files, version=version_str, message=message, log=log)

    log.warning(f"Version updated: {previous_version_str} > {version_str}")
