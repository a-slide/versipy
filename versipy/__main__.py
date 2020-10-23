#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~IMPORTS~~~~~~~~~~~~~~#
# Standard library imports
import argparse
import sys

# Local imports
import versipy as pkg
from versipy.common import *
from versipy.versipy import init, current_version, bump_up_version, set_version  # ,  git_tag

# ~~~~~~~~~~~~~~TOP LEVEL ENTRY POINT~~~~~~~~~~~~~~#
def main(args=None):
    """ Main entry point for versipy command line interface"""

    # Parser and subparsers for command
    parser = argparse.ArgumentParser(description=pkg.__description__)
    parser.add_argument("--version", action="version", version="{} v{}".format(pkg.__name__, pkg.__version__))
    subparsers = parser.add_subparsers(description="%(prog)s implements the following subcommands", dest="subcommands")
    subparsers.required = True

    f = init
    sp_init = subparsers.add_parser("init", description=doc_func(f))
    sp_init.set_defaults(func=f)

    f = current_version
    sp_cv = subparsers.add_parser("current_version", description=doc_func(f))
    sp_cv.set_defaults(func=f)
    arg_from_docstr(sp_cv, f, "versipy_fn")

    f = bump_up_version
    sp_bv = subparsers.add_parser("bump_up_version", description=doc_func(f))
    sp_bv.set_defaults(func=f)
    arg_from_docstr(sp_bv, f, "versipy_fn")
    sp_bv_opt = sp_bv.add_argument_group("Versioning options")
    arg_from_docstr(sp_bv_opt, f, "major", "M")
    arg_from_docstr(sp_bv_opt, f, "minor", "m")
    arg_from_docstr(sp_bv_opt, f, "micro", "u")
    arg_from_docstr(sp_bv_opt, f, "a")
    arg_from_docstr(sp_bv_opt, f, "b")
    arg_from_docstr(sp_bv_opt, f, "release_candidate", "r")
    arg_from_docstr(sp_bv_opt, f, "post", "p")
    arg_from_docstr(sp_bv_opt, f, "dev", "d")
    sp_bv_git = sp_bv.add_argument_group("Git options")
    arg_from_docstr(sp_bv_opt, f, "git_tag", "t")
    sp_bv_git = sp_bv.add_argument_group("Git options")
    arg_from_docstr(sp_bv_opt, f, "m", "c")

    f = set_version
    sp_sv = subparsers.add_parser("set_version", description=doc_func(f))
    sp_sv.set_defaults(func=f)
    arg_from_docstr(sp_sv, f, "versipy_fn")

    # Add common group parsers
    for sp in [sp_init, sp_bv, sp_cv, sp_sv]:
        sp_vb = sp.add_argument_group("Verbosity options")
        sp_vb.add_argument("-v", "--verbose", action="store_true", default=False, help="Increase verbosity")
        sp_vb.add_argument("-q", "--quiet", action="store_true", default=False, help="Reduce verbosity")

    # Parse args and call subfunction
    args = parser.parse_args()
    args.func(**vars(args))
