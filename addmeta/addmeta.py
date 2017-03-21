#!/usr/bin/env python

import errno
import yaml
import collections
import xarray
import netCDF4 as nc
import six

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

    try:
        with open(fname, 'r') as yaml_file:
            metadict = yaml.load(yaml_file)
    except IOError as exc:
        if exc.errno == errno.ENOENT:
            print('payu: warning: yaml file {0} not found!'
                  .format(fname))
            metadict = {}
        else:
            raise

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


def find_and_add_meta(ncfiles, metafiles):
    """Add meta data from 1 or more yaml formatted files to one or more
    netCDF files
    """

    metadata = combine_meta(metafiles)

    for fname in ncfiles:
        add_meta(fname, metadata)
        
    
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Add meta data to one or more netCDF files")
    parser.add_argument("inputs", help="netCDF files or directories (-r must be specified to recursively descend directories)", nargs='+')
    args = parser.parse_args()
