#!/usr/bin/env python


"""
Copyright 2015 ARC Centre of Excellence for Climate Systems Science

author: Aidan Heerdegen <aidan.heerdegen@anu.edu.au>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


from __future__ import print_function

import pytest
import sys
import os
import shutil
import subprocess
import shlex
import copy

# Find the python libraries we're testing
sys.path.append('..')
sys.path.append('.')

from addmeta import read_yaml, dict_merge, combine_meta, add_meta, find_and_add_meta, skip_comments, list_from_file

verbose = True

def runcmd(cmd):
    subprocess.check_call(shlex.split(cmd),stderr=subprocess.STDOUT)

def setup_module(module):
    if verbose: print ("setup_module      module:%s" % module.__name__)
    cmd = "ncgen -o test/test.nc test/test.cdl"
    runcmd(cmd)
 
def teardown_module(module):
    if verbose: print ("teardown_module   module:%s" % module.__name__)
    cmd = "rm test/test.nc"
#    runcmd(cmd)

def test_read_yaml():
    if verbose:  print("\nIn test_read_yaml")

    dict1 = read_yaml("test/meta1.yaml")

    assert(dict1 == {'global': {'Publisher': 'ARC Centre of Excellence for Climate System Science', 'Year': 2017}})

    dict2 = read_yaml("test/meta2.yaml")

    assert(dict2 == {'global': {'Publisher': 'ARC Centre of Excellence for Climate System Science (ARCCSS)', 'Credit': 'NCI'}})

    dictcombined = copy.deepcopy(dict2)

    dict_merge(dictcombined,dict1)

    assert(dictcombined == {'global': {'Publisher': 'ARC Centre of Excellence for Climate System Science', 'Year': 2017, 'Credit': 'NCI'}})

    dictcombined = {}
    dictcombined = combine_meta(('test/meta2.yaml','test/meta1.yaml'))

    assert(dictcombined == {'global': {'Publisher': 'ARC Centre of Excellence for Climate System Science', 'Year': 2017, 'Credit': 'NCI'}})

    # Unfortunately when yaml files are concatenated, subsequent values overwrite
    # previous entries, so this is equivalent to dict2
    dictcat = read_yaml("test/meta12.yaml")

    assert(dictcat == dict2)

def test_metadata():

    metadata_dir = 'metadata'

    for root, dirs, files in os.walk(metadata_dir):
        for fname in files:
            path = os.path.join(root,fname)
            print("Reading {}".format(path))
            dict = read_yaml(path)

def test_skipcomments():

    fname = 'test/metalist'
    with open(fname, 'rt') as f:
        filelist = tuple(skip_comments(f))

    assert(filelist == ('meta1.yaml', 'meta2.yaml'))
    
def test_list_from_file():

    fname = 'test/metalist'
    filelist = list_from_file(fname)
    assert(filelist == ('meta1.yaml', 'meta2.yaml'))
    

def test_add_meta():
    
    dict1 = read_yaml("test/meta1.yaml")

    add_meta('test/test.nc', dict1)


def test_find_add_meta():
    
    find_and_add_meta(['test/meta2.yaml','test/meta1.yaml'], ['test/test.nc'])
