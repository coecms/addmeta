#!/usr/bin/env python

from __future__ import print_function

import errno
import yaml
import collections
import netCDF4 as nc
import six
import argparse

# From https://gist.github.com/angstwad/bf22d1822c38a92ec0a9
def dict_merge(dct, merge_dct):
    """ Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
    updating only top-level keys, dict_merge recurses down into dicts nested
    to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
    ``dct``.
    :param dct: dict onto which the merge is executed
    :param merge_dct: dct merged into dct
    :return: None
    """
    for k, v in six.iteritems(merge_dct):
        if (k in dct and isinstance(dct[k], dict)
                and isinstance(merge_dct[k], collections.Mapping)):
            dict_merge(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]

def read_yaml(fname):
    """Parse yaml file and return a dict."""

    with open(fname, 'r') as yaml_file:
        metadict = yaml.load(yaml_file)

    return metadict

def combine_meta(fnames):
    """Read multiple yaml files containing meta data and combine their
    dictionaries. The order of the files is the reverse order of preference, so
    files listed later overwrite fields from files list earlier"""

    allmeta = {}

    for fname in fnames:
        meta = read_yaml(fname)
        dict_merge(allmeta, meta)

    return allmeta

def add_meta(ncfile, metadict):
    """Add meta data from a dictionary to a netCDF file
    """

    rootgrp = nc.Dataset(ncfile, "r+")
    rootgrp.setncatts(metadict["global"])
    rootgrp.close()


def find_and_add_meta(metafiles, ncfiles):
    """Add meta data from 1 or more yaml formatted files to one or more
    netCDF files
    """

    metadata = combine_meta(metafiles)

    for fname in ncfiles:
        add_meta(fname, metadata)
        
def skip_comments(file):
    """Skip lines that begin with a comment character (#) or are empty
    """
    for line in file:
        sline = line.strip()
        if not sline.startswith('#') and not sline == '':
            yield sline
    
def list_from_file(fname):
    with open(fname, 'rt') as f:
        filelist = tuple(skip_comments(f))
    return(filelist)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Add meta data to one or more netCDF files")
    parser.add_argument("-m","--metafiles", help="One or more meta-data files in YAML format", action='append')
    parser.add_argument("-l","--metalist", help="File containing a list of meta-data files")
    parser.add_argument("-v","--verbose", help="Verbose output", action='store_true')
    parser.add_argument("files", help="netCDF files", nargs='+')
    args = parser.parse_args()

    verbose = args.verbose

    metafiles = []
    if (args.metafiles is not None):
        metafiles.extend(args.metafiles)

    if (args.metalist is not None):
        metafiles.extend(list_from_file(args.metalist))

    if verbose: print("metafiles: "," ".join(metafiles))

    find_and_add_meta(metafiles, args.files)
