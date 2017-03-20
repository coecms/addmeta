#!/usr/bin/env python

import errno
import yaml
import collections

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
    for k, v in merge_dct.iteritems():
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
    dictionaries. The order of the files is the order of preference, so
    files listed later will have their fields overwritten by files list earlier"""

    allmeta = {}

    for fname in fnames:
        meta = read_yaml(fname)
        dict_merge(allmeta, meta)

    return allmeta
        
    

