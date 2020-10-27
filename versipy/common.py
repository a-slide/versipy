# -*- coding: utf-8 -*-

# IMPORTS ##############################################################################################################

# Standard library imports
import logging
import os
import re
import sys
import inspect
import datetime
from collections import OrderedDict, Counter
import copy
import string

# Third party imports
import colorlog
from git import Repo
import yaml

# Local imports
import versipy as pkg


# BASIC TOOLS FUNCTIONS ################################################################################################


def stdout_print(*args):
    """
    Emulate print but uses sys stdout instead.
    """
    s = " ".join([str(i) for i in args])
    sys.stdout.write(s)
    sys.stdout.flush()


def opt_summary(local_opt):
    """Simplifiy option dict creation"""
    d = OrderedDict()
    d["Package name"] = pkg.__name__
    d["Package version"] = pkg.__version__
    d["Timestamp"] = str(datetime.datetime.now())
    for i, j in local_opt.items():
        d[i] = j
    return d


def mkdir(fn, exist_ok=False):
    """ Create directory recursivelly. Raise IO error if path exist or if error at creation """
    try:
        os.makedirs(fn, exist_ok=exist_ok)
    except:
        raise pycoMethError("Error creating output folder `{}`".format(fn))


def mkbasedir(fn, exist_ok=False):
    """ Create directory for a given file recursivelly. Raise IO error if path exist or if error at creation """
    dir_fn = os.path.dirname(fn)
    if dir_fn:
        mkdir(dir_fn, exist_ok=True)


def check_access(fn, read=False, write=False):
    try:
        if read and not os.access(fn, os.R_OK):
            return False
        if write and not os.access(fn, os.W_OK):
            return False
        return True
    except:
        return False


def choose_option(choices=["y", "n"], message="Choose a valid option"):
    while True:
        x = input("{} [{}]".format(message, ",".join(choices)))
        if x in choices:
            return x
        else:
            print("{} is not a valid option".format(x))


# LOGGING FUNCTIONS ####################################################################################################


def get_logger(name=None, verbose=False, quiet=False):
    """Multilevel colored log using colorlog"""

    # Define conditional color formatter
    formatter = colorlog.LevelFormatter(
        fmt={
            "DEBUG": "%(log_color)s\t[DEBUG]: %(msg)s",
            "INFO": "%(log_color)s\t%(msg)s",
            "WARNING": "%(log_color)s## %(msg)s ##",
            "ERROR": "%(log_color)sERROR: %(msg)s",
            "CRITICAL": "%(log_color)sCRITICAL: %(msg)s",
        },
        log_colors={
            "DEBUG": "white",
            "INFO": "green",
            "WARNING": "bold_blue",
            "ERROR": "bold_red",
            "CRITICAL": "bold_purple",
        },
        reset=True,
    )

    # Define logger with custom formatter
    logging.basicConfig(format="%(message)s")
    logging.getLogger().handlers[0].setFormatter(formatter)
    log = logging.getLogger(name)

    # Define logging level depending on verbosity
    if verbose:
        log.setLevel(logging.DEBUG)
    elif quiet:
        log.setLevel(logging.WARNING)
    else:
        log.setLevel(logging.INFO)

    return log


def log_dict(d, logger, header="", indent="\t", level=1):
    """ log a multilevel dict """
    if header:
        logger(header)
    if isinstance(d, Counter):
        for i, j in d.most_common():
            logger("{}{}: {:,}".format(indent * level, i, j))
    else:
        for i, j in d.items():
            if isinstance(j, dict):
                logger("{}{}".format(indent * level, i, j))
                log_dict(j, logger, level=level + 1)
            else:
                logger("{}{}: {}".format(indent * level, i, j))


def log_list(l, logger, header="", indent="\t"):
    """ log a list """
    if header:
        logger(header)
    for i in l:
        logger("{}*{}".format(indent, i))


# ARGUMENT PARSING FUNCTIONS ###########################################################################################


def doc_func(func):
    """Parse the function description string"""

    if inspect.isclass(func):
        func = func.__init__

    docstr_list = []
    for l in inspect.getdoc(func).split("\n"):
        l = l.strip()
        if l:
            if l.startswith("*"):
                break
            else:
                docstr_list.append(l)

    return " ".join(docstr_list)


def make_arg_dict(func):
    """Parse the arguments default value, type and doc"""

    # Init method for classes
    if inspect.isclass(func):
        func = func.__init__

    if inspect.isfunction(func) or inspect.ismethod(func):
        # Parse arguments default values and annotations
        d = OrderedDict()
        for name, p in inspect.signature(func).parameters.items():
            if not p.name in ["self", "cls"]:  # Object stuff. Does not make sense to include in doc
                d[name] = OrderedDict()
                if not name in ["kwargs", "args"]:  # Include but skip default required and type
                    # Get Annotation
                    if p.annotation != inspect._empty:
                        d[name]["type"] = p.annotation
                    # Get default value if available
                    if p.default == inspect._empty:
                        d[name]["required"] = True
                    else:
                        d[name]["default"] = p.default

        # Parse the docstring in a dict
        docstr_dict = OrderedDict()
        lab = None
        for l in inspect.getdoc(func).split("\n"):
            l = l.strip()
            if l:
                if l.startswith("*"):
                    lab = l[1:].strip()
                    docstr_dict[lab] = []
                elif lab:
                    docstr_dict[lab].append(l)

        # Concatenate and copy doc in main dict
        for name in d.keys():
            if name in docstr_dict:
                d[name]["help"] = " ".join(docstr_dict[name])
        return d


def arg_from_docstr(parser, func, arg_name, short_name=None):
    """Get options corresponding to argument name from docstring and deal with special cases"""

    if short_name:
        arg_names = ["-{}".format(short_name), "--{}".format(arg_name)]
    else:
        arg_names = ["--{}".format(arg_name)]

    arg_dict = make_arg_dict(func)[arg_name]
    if "help" in arg_dict:
        if "default" in arg_dict:
            if arg_dict["default"] == "" or arg_dict["default"] == []:
                arg_dict["help"] += " (default: None)"
            else:
                arg_dict["help"] += " (default: %(default)s)"
        else:
            arg_dict["help"] += " (required)"

        if "type" in arg_dict:
            if arg_dict["type"] == bool:
                arg_dict["help"] += " [boolean]"
            else:
                arg_dict["help"] += " [%(type)s]"

    # Special case for boolean args
    if arg_dict["type"] == bool:
        if arg_dict["default"] == False:
            arg_dict["action"] = "store_true"
            del arg_dict["type"]
        elif arg_dict["default"] == True:
            arg_dict["action"] = "store_false"
            del arg_dict["type"]

    # Special case for lists args
    elif isinstance(arg_dict["type"], list):
        arg_dict["nargs"] = "*"
        arg_dict["type"] = arg_dict["type"][0]

    parser.add_argument(*arg_names, **arg_dict)


# YAML IO OPTIONS ######################################################################################################


def ordered_load_yaml(yaml_fn, Loader=yaml.Loader, **kwargs):
    """
    Ensure YAML entries are loaded in an ordered dict following the original file order
    """
    # Define custom loader
    class OrderedLoader(Loader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return OrderedDict(loader.construct_pairs(node))

    OrderedLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)
    # Try to load file
    try:
        with open(yaml_fn, "r") as yaml_fp:
            d = yaml.load(stream=yaml_fp, Loader=OrderedLoader, **kwargs)
            return d
    except:
        raise IOError("YAML file does not exist or is not valid: {}".format(yaml_fn))


def ordered_dump_yaml(d, yaml_fn, Dumper=yaml.Dumper, **kwargs):
    """
    Ensure ordered dict items are dumped in YAML file following the dictionary order
    """
    # Define custom dumper
    class OrderedDumper(Dumper):
        pass

    def _dict_representer(dumper, data):
        return dumper.represent_mapping(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, data.items())

    OrderedDumper.add_representer(OrderedDict, _dict_representer)

    # Try to dump dict to file
    try:
        with open(yaml_fn, "w") as yaml_fp:
            yaml.dump(data=d, stream=yaml_fp, Dumper=OrderedDumper, **kwargs)
    except:
        raise IOError("Error while trying to dump data in file: {}".format(yaml_fn))


# VERSIPY SPECIFIC FUNCTIONS ###########################################################################################


def is_canonical_version(version):
    RE = re.compile(
        "^([1-9][0-9]*!)?(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))*((a|b|rc)(0|[1-9][0-9]*))?(\.post(0|[1-9][0-9]*))?(\.dev(0|[1-9][0-9]*))?$"
    )
    return re.match(RE, version) is not None


def get_version_str(d):
    # minimal version
    s = "{}".format(d["major"])
    # optional minor and micro numbers
    if d["minor"] is not None:
        s += ".{}".format(d["minor"])
    if d["micro"] is not None:
        s += ".{}".format(d["micro"])
    # optional release type version
    if d["rc"] is not None:
        s += "rc{}".format(d["rc"])
    elif d["b"] is not None:
        s += "b{}".format(d["b"])
    elif d["a"] is not None:
        s += "a{}".format(d["a"])
    # optional post and dev tags
    if d["post"] is not None:
        s += ".post{}".format(d["post"])
    if d["dev"] is not None:
        s += ".dev{}".format(d["dev"])
    return s


def get_versipy_yaml(versipy_fn, log):
    """load end check versipy file"""

    # Try to load YAML file
    log.debug("Loading versipy YAML file")
    info_d = ordered_load_yaml(versipy_fn)

    # Check that all fields are there
    log.debug("Checking file structure")
    for field in ["version", "managed_values", "managed_files"]:
        if not field in info_d:
            raise ValueError("Missing section '{}' in versipy YAML file".format(field))
        if not info_d[field]:
            raise ValueError("Empty section '{}' in versipy YAML file".format(field))

    # Verify validity of version string
    log.debug("Checking version")
    for field in ["major", "minor", "micro", "a", "b", "rc", "post", "dev"]:
        if not field in info_d["version"]:
            raise ValueError("Missing field '{}' in versipy YAML file version section".format(field))
    version_str = get_version_str(info_d["version"])
    if not is_canonical_version(version_str):
        raise ValueError("Current version {} is not a valid PEP canonical version".format(version_str))

    return info_d


def reset_version(version_d, levels):
    for level in levels:
        if level == "minor" and version_d["minor"] is not None:
            version_d["minor"] = 0
        elif level == "micro" and version_d["micro"] is not None:
            version_d["micro"] = 0
        else:
            version_d[level] = None
    return version_d


def increment_version(
    version_d,
    log,
    major=False,
    minor=False,
    micro=False,
    a=False,
    b=False,
    rc=False,
    post=False,
    dev=False,
):

    # safe increment variable even if None
    def increment_safe(v):
        return 1 if v is None else v + 1

    version_d = copy.deepcopy(version_d)
    if major:
        log.debug("Increment major level and reset all lower levels")
        version_d["major"] = increment_safe(version_d["major"])
        version_d = reset_version(version_d, levels=["minor", "micro", "a", "b", "rc", "post", "dev"])
    if minor:
        log.debug("Increment minor level and reset all lower levels")
        version_d["minor"] = increment_safe(version_d["minor"])
        version_d = reset_version(version_d, levels=["micro", "a", "b", "rc", "post", "dev"])

    # optional micro version number
    if micro:
        log.debug("Increment micro level and reset all lower levels")
        version_d["micro"] = increment_safe(version_d["micro"])
        version_d = reset_version(version_d, levels=["a", "b", "rc", "post", "dev"])

    # optional release type version
    if rc:
        log.debug("Increment rc level and reset all lower levels")
        version_d["rc"] = increment_safe(version_d["rc"])
        version_d = reset_version(version_d, levels=["a", "b", "post", "dev"])
    elif b:
        log.debug("Increment b level and reset all lower levels")
        version_d["b"] = increment_safe(version_d["b"])
        version_d = reset_version(version_d, levels=["a", "rc", "post", "dev"])
    elif a:
        log.debug("Increment a level and reset all lower levels")
        version_d["a"] = increment_safe(version_d["a"])
        version_d = reset_version(version_d, levels=["b", "rc", "post", "dev"])

    # optional post and dev tags
    if post:
        log.debug("Increment post level and reset all lower levels")
        version_d["post"] = increment_safe(version_d["post"])
    if dev:
        log.debug("Increment dev level and reset all lower levels")
        version_d["dev"] = increment_safe(version_d["dev"])

    # sanity check
    version_str = get_version_str(version_d)
    if not is_canonical_version(version_str):
        raise ValueError("Current version {version_str} is not a valid PEP canonical version")

    log_dict(version_d, log.debug, "Updated version values")
    return version_d


def parse_version_str(version_str, log):
    """"""
    if not is_canonical_version(version_str):
        raise ValueError("Current version {version_str} is not a valid PEP canonical version")

    log.debug("Split version number into a list")
    alphabet = list(string.ascii_letters)
    l = []
    s = ""
    for c in version_str:
        if c == ".":
            if s:
                l.append(s)
                s = ""
        elif c in alphabet:
            if s and not s[-1] in alphabet:
                l.append(s)
                s = ""
            s += c
        elif c.isdigit():
            s += c
    l.append(s)

    log.debug("Store list values in version dictionary")
    version_d = OrderedDict(major=0, minor=None, micro=None, a=None, b=None, rc=None, post=None, dev=None)
    if l[0].isdigit():
        version_d["major"] = int(l[0])
    if len(l) >= 2 and l[1].isdigit():
        version_d["minor"] = int(l[1])
    if len(l) >= 3 and l[2].isdigit():
        version_d["micro"] = int(l[2])
    for e in l:
        for tag in ["a", "b", "rc", "dev", "post"]:
            if e.startswith(tag):
                version_d[tag] = int(e.strip(tag))
                break

    log_dict(version_d, log.debug, "Updated version values")
    return version_d


def update_managed_files(info_d, overwrite, dry, log):
    """"""
    version_str = get_version_str(info_d["version"])

    for src_fn, dest_fn in info_d["managed_files"].items():
        log.debug("Updating file {}".format(dest_fn))

        # Bulletproof reading and writing
        try:
            src_fp = dest_fp = None

            # Open template file for reading
            try:
                src_fp = open(src_fn, "r")
            except:
                raise IOError("Cannot read source Template file: {}".format(src_fn))

            # Open destination file for writing
            if not dry:
                try:
                    if not overwrite and os.path.isfile(dest_fn):
                        choice = choose_option(
                            choices=["y", "n"], message="Overwrite existing file {} ?".format(dest_fn)
                        )
                        if choice == "n":
                            log.debug("File {dest_fn} was skipped")
                            continue
                    dest_fp = open(dest_fn, "w")
                except:
                    raise IOError("Cannot write to destination file: {}".format(dest_fn))

            s = src_fp.read()
            s = s.replace("__package_version__", version_str)
            for k, v in info_d["managed_values"].items():
                s = s.replace(k, v)

            if dry:
                stdout_print(s)
            else:
                dest_fp.write(s)

        finally:
            # Try to close file pointers
            for fp, fn in [[src_fp, src_fn], [dest_fp, dest_fn]]:
                if fp:
                    try:
                        fp.close()
                    except:
                        pass


def update_versipy_files(info_d, versipy_fn, versipy_history_fn, comment, overwrite, dry, log):
    """"""
    version_str = get_version_str(info_d["version"])
    if not dry:
        choice = "y"
        if os.path.isfile(versipy_fn) and not overwrite:
            choice = choose_option(choices=["y", "n"], message="Overwrite existing versipy files?")
        if choice == "n":
            log.debug("Versipy files were not updated")
        elif choice == "y":
            log.debug("Updating versipy template yaml file")
            ordered_dump_yaml(info_d, versipy_fn, Dumper=yaml.Dumper)
            log.debug("Updating versipy history file")
            with open(versipy_history_fn, "a") as fp:
                fp.write("{}\t{}\t{}\n".format(datetime.datetime.now(), version_str, comment))


def get_versipy_yaml_template():
    info_d = OrderedDict()

    # Version section
    info_d["version"] = OrderedDict()
    info_d["version"]["major"] = 0
    info_d["version"]["minor"] = 0
    info_d["version"]["micro"] = 0
    info_d["version"]["a"] = None
    info_d["version"]["b"] = None
    info_d["version"]["rc"] = None
    info_d["version"]["post"] = None
    info_d["version"]["dev"] = None

    # Managed values section
    info_d["managed_values"] = OrderedDict()
    info_d["managed_values"]["__package_name__"] = "package name"
    info_d["managed_values"]["__package_description__"] = "package description"
    info_d["managed_values"]["__package_url__"] = "package URL"
    info_d["managed_values"]["__package_licence__"] = "package licence"
    info_d["managed_values"]["__author_name__"] = "author name"
    info_d["managed_values"]["__author_email__"] = "author contact email"

    # Managed files section
    info_d["managed_files"] = OrderedDict()
    info_d["managed_files"]["versipy_templates/setup.py"] = "setup.py"
    info_d["managed_files"]["versipy_templates/meta.yaml"] = "meta.yaml"
    info_d["managed_files"]["versipy_templates/__init__.py"] = "versipy/__init__.py"
    info_d["managed_files"]["versipy_templates/README.md"] = "README.md"

    return info_d


def write_versipy_yaml(versipy_fn, overwrite, log):

    info_d = versipy_info_d()
    log_dict(info_d, log.debug, "template info dict")

    # Open destination file for writing
    log.debug("Try to dump data to YAML file {}".format(versipy_fn))
    if not overwrite and os.path.isfile(versipy_fn):
        choice = choose_option(choices=["y", "n"], message="Overwrite existing file {} ?".format(versipy_fn))
        if choice == "n":
            log.debug("File {} was skipped".format(versipy_fn))
            return
    ordered_dump_yaml(info_d, versipy_fn)


def git_files(files, version, comment, git_tag, log):
    """"""
    try:
        log.debug("Acquire local repository")
        repo = Repo()
        remote = repo.remote("origin")

        log.debug("Add, commit and push version files")
        for f in files:
            repo.index.add(f)
        commit = repo.index.commit(message=comment)
        push = remote.push()

        if git_tag:
            log.debug("Set and push new version tag")
            tag = repo.create_tag(version, message=comment)
            push = remote.push(tag)

    except Exception as E:
        log.info("Failed to push to remote")
        log.debug(type(E), str(E))
