#!/usr/bin/env python

import argparse
import json
import tempfile
import os
import subprocess
from collections import OrderedDict

parser = argparse.ArgumentParser()
parser.add_argument("a", help="First File to Diff")
parser.add_argument("b", help="Second File to Diff")
parser.add_argument("-d", "--difftool", help="Diff Tool to use", required=True)
args = parser.parse_args()

def diff(a, b, difftool):
    subprocess.Popen([difftool, _load_file(a), _load_file(b)])
    print 'You should periodically clear the /tmp/tmp* files from your system to prevent interesting ASCII art :-)'


def _load_file(name):
    file_contents = ''
    with open(os.path.realpath(name)) as file_name:
        # load in the JSON template into a Python object
        loaded_template = json.load(file_name)
        # sort it
        sorted_template = walk_and_sort(loaded_template)
        # output the sorted object back to JSON for human-viewable diffing
        file_contents = json.dumps(sorted_template, indent=4, sort_keys=True)

    # smash the output into a temporary file, so we can call meld on it
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=name.replace('/', '_'))
    temp_file.file.write(file_contents)
    temp_file.close()

    return temp_file.name


def walk_and_sort(coll):
    if isinstance(coll, dict):
        return OrderedDict([(k,v) for k,v in sorted(
                    map(lambda kv: (kv[0], walk_and_sort(kv[1])), coll.iteritems()), key=lambda k: k[0])])

    elif isinstance(coll, list):
        return sorted(list(map(walk_and_sort, coll)))

    return coll

(__name__ == '__main__' and diff(args.a, args.b, args.difftool))
