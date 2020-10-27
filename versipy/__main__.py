#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~IMPORTS~~~~~~~~~~~~~~#
# Standard library imports
import argparse
import sys

# Local imports
import versipy as pkg
from versipy.common import *
from versipy.versipy import init_repo, current_version, bump_up_version, set_version  # ,  git_tag

# ~~~~~~~~~~~~~~TOP LEVEL ENTRY POINT~~~~~~~~~~~~~~#
def main(args=None):
    """ Main entry point for versipy command line interface"""

    # Parser and subparsers for command
    parser = argparse.ArgumentParser(description=pkg.__description__)
    parser.add_argument("--version", action="version", version="{} v{}".format(pkg.__name__, pkg.__version__))
    subparsers = parser.add_subparsers(description="%(prog)s implements the following subcommands", dest="subcommands")
    subparsers.required = True

    f = init_repo
    sp_init = subparsers.add_parser("init_repo", description=doc_func(f))
    sp_init.set_defaults(func=f)
    sp_init_io = sp_init.add_argument_group("IO options")
    arg_from_docstr(sp_init_io, f, "versipy_fn")
    arg_from_docstr(sp_init_io, f, "versipy_history_fn")
    arg_from_docstr(sp_init_io, f, "overwrite", "o")

    f = current_version
    sp_cv = subparsers.add_parser("current_version", description=doc_func(f))
    sp_cv.set_defaults(func=f)
    sp_cv_io = sp_cv.add_argument_group("IO options")
    arg_from_docstr(sp_cv_io, f, "versipy_fn")

    f = bump_up_version
    sp_bv = subparsers.add_parser("bump_up_version", description=doc_func(f))
    sp_bv.set_defaults(func=f)
    sp_bv_opt = sp_bv.add_argument_group("Versioning options")
    arg_from_docstr(sp_bv_opt, f, "major", "M")
    arg_from_docstr(sp_bv_opt, f, "minor", "m")
    arg_from_docstr(sp_bv_opt, f, "micro", "u")
    arg_from_docstr(sp_bv_opt, f, "alpha", "a")
    arg_from_docstr(sp_bv_opt, f, "beta", "b")
    arg_from_docstr(sp_bv_opt, f, "rc", "r")
    arg_from_docstr(sp_bv_opt, f, "post", "p")
    arg_from_docstr(sp_bv_opt, f, "dev", "d")
    sp_bv_io = sp_bv.add_argument_group("IO options")
    arg_from_docstr(sp_bv_io, f, "versipy_fn")
    arg_from_docstr(sp_bv_io, f, "versipy_history_fn")
    arg_from_docstr(sp_bv_io, f, "overwrite", "o")
    sp_bv_ms = sp_bv.add_argument_group("Misc options")
    arg_from_docstr(sp_bv_ms, f, "git_push", "g")
    arg_from_docstr(sp_bv_ms, f, "git_tag", "t")
    arg_from_docstr(sp_bv_ms, f, "comment", "c")
    arg_from_docstr(sp_bv_ms, f, "dry")

    f = set_version
    sp_sv = subparsers.add_parser("set_version", description=doc_func(f))
    sp_sv.set_defaults(func=f)
    sp_bv_opt = sp_sv.add_argument_group("Versioning options")
    arg_from_docstr(sp_bv_opt, f, "version_str", "s")
    sp_sv_io = sp_sv.add_argument_group("IO options")
    arg_from_docstr(sp_sv_io, f, "versipy_fn")
    arg_from_docstr(sp_sv_io, f, "versipy_history_fn")
    arg_from_docstr(sp_sv_io, f, "overwrite", "o")
    sp_sv_ms = sp_sv.add_argument_group("Misc options")
    arg_from_docstr(sp_sv_ms, f, "git_push", "g")
    arg_from_docstr(sp_bv_ms, f, "git_tag", "t")
    arg_from_docstr(sp_sv_ms, f, "comment", "c")
    arg_from_docstr(sp_sv_ms, f, "dry")

    # Add common group parsers
    for sp in [sp_init, sp_bv, sp_cv, sp_sv]:
        sp_vb = sp.add_argument_group("Verbosity options")
        sp_vb.add_argument("-v", "--verbose", action="store_true", default=False, help="Increase verbosity")
        sp_vb.add_argument("-q", "--quiet", action="store_true", default=False, help="Reduce verbosity")

    # Parse args and call subfunction
    args = parser.parse_args()
    args.func(**vars(args))
