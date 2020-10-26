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


def init_repo(
    versipy_fn: str = "versipy.yaml",
    versipy_history_fn: str = "versipy_history.txt",
    overwrite: bool = False,
    verbose: bool = False,
    quiet: bool = False,
    **kwargs,
):
    """
    * versipy_fn
        Path to write a template versipy YAML file
    * versipy_history_fn
        Path to write a the versipy history file
    * overwrite
        Do not display a confirmation message before overwriting an existing file
    """
    # Init method
    opt_summary_dict = opt_summary(local_opt=locals())
    log = get_logger(name="versipy init_repo", verbose=verbose, quiet=quiet)

    log.warning("Generating example template versipy YAML file")
    log_dict(opt_summary_dict, log.debug, "Options summary")

    info_d = get_versipy_yaml_template()

    update_versipy_files(
        info_d=info_d,
        versipy_fn=versipy_fn,
        versipy_history_fn=versipy_history_fn,
        message="Initialise versipy history",
        overwrite=overwrite,
        dry=False,
        log=log,
    )


def current_version(versipy_fn: str = "versipy.yaml", verbose: bool = False, quiet: bool = False, **kwargs):
    """
    Return the current package version
    * versipy_fn
        Path to the versipy YAML info file containing package metadata
    """
    # Init method
    opt_summary_dict = opt_summary(local_opt=locals())
    log = get_logger(name="versipy bump_up", verbose=verbose, quiet=quiet)

    log.warning("Bumping up version package version")
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
    alpha: bool = False,
    beta: bool = False,
    rc: bool = False,
    post: bool = False,
    dev: bool = False,
    versipy_fn: str = "versipy.yaml",
    versipy_history_fn: str = "versipy_history.txt",
    overwrite: bool = False,
    git_push: bool = False,
    message: str = "Versipy auto bump-up",
    dry: bool = False,
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
    * alpha
        Increment the alpha (a) version level by 1
    * beta
        Increment the beta (b) version level by 1
    * rc
        Increment the release candidate (rc) version level by 1
    * post
        Increment the major post level by 1
    * dev
        Increment the major dev level by 1
    * versipy_fn
        Path to the versipy YAML info file containing package metadata
    * versipy_history_fn
        Path to the versipy history file
    * overwrite
        Do not display a confirmation message before overwriting an existing file
    * git_push
        Commit and push the files modified by versipy and set a git version tag
    * message
        Message used for the history file and the git commit is used in combination with `git_push`
    * dry
        Dry run, simulate version update but don't change files
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
        version_d=info_d["version"],
        major=major,
        minor=minor,
        micro=micro,
        a=alpha,
        b=beta,
        rc=rc,
        post=post,
        dev=dev,
        log=log,
    )
    version_str = get_version_str(info_d["version"])

    log.info("Update managed files")
    update_managed_files(info_d=info_d, overwrite=overwrite, dry=dry, log=log)
    update_versipy_files(
        info_d=info_d,
        versipy_fn=versipy_fn,
        versipy_history_fn=versipy_history_fn,
        message=message,
        overwrite=overwrite,
        dry=dry,
        log=log,
    )

    # Optional git tagging
    if git_push and not dry:
        log.info("Attempting set tag and to push files to remote repository")
        managed_files = [f for f in info_d["managed_files"].values()]
        extra_files = [versipy_fn, versipy_history_fn]
        git_files(files=managed_files + extra_files, version=version_str, message=message, log=log)

    log.warning("Version updated: {} > {}".format(previous_version_str, version_str))


def set_version(
    version_str: str,
    versipy_fn: str = "versipy.yaml",
    versipy_history_fn: str = "versipy_history.txt",
    overwrite: bool = False,
    git_push: bool = False,
    message: str = "Manually set version",
    dry: bool = False,
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
    * versipy_fn
        Path to the versipy YAML info file containing package metadata
    * versipy_history_fn
        Path to the versipy history file
    * overwrite
        Do not display a confirmation message before overwriting an existing file
    * git_push
        Commit and push the files modified by versipy and set a git version tag
    * message
        Message used for the history file and the git commit is used in combination with `git_push`
    * dry
        Dry run, simulate version update but don't change files
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
    update_managed_files(info_d=info_d, overwrite=overwrite, dry=dry, log=log)
    update_versipy_files(
        info_d=info_d,
        versipy_fn=versipy_fn,
        versipy_history_fn=versipy_history_fn,
        message=message,
        overwrite=overwrite,
        dry=dry,
        log=log,
    )

    # Optional git tagging
    if git_push and not dry:
        log.info("Attempting set tag and to push files to remote repository")
        managed_files = [f for f in info_d["managed_files"].values()]
        extra_files = [versipy_fn, versipy_history_fn]
        git_files(files=managed_files + extra_files, version=version_str, message=message, log=log)

    log.warning("Version updated: {} > {}".format(previous_version_str, version_str))
