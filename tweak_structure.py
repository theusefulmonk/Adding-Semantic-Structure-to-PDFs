#!/usr/bin/env python

# This script will provide the ability to edit in the nodes of a pdf table of
# contents in json formt.
# It is designed for optional use in a shell pipeline
# But can be invoked with a filename argument to look up a previously generated
# toc in the cache

import sys
import os
import json
from pprint import pprint
from shutil import get_terminal_size
import argparse
import shelve

# Functions
# source: https://gist.github.com/mattmc3/cb62868e0ec068c62c36e9d7aa85c6c7
def stdin_is_piped():
    fileno = sys.stdin.fileno()
    mode = os.fstat(fileno).st_mode
    return not os.isatty(fileno) and stat.S_ISFIFO(mode)

def legibly_print(bookmark_list):
    for i in bookmark_list:
        representation = " " + str(bookmark_list.index(i) + 1) + ". " + str(i)
        print(representation)

def needs_pager(bookmark_list):
    current_terminal_height = get_terminal_size()[1]
    OFFSET = 5
    if len(bookmark_list) > current_terminal_height - OFFSET:
        return True
    else:
        return False

def delete_node(n):
    OFFSET = -1
    to_delete = n + OFFSET
    del bookmarks[to_delete]

def keep_node(n):
    if n not in nodes_to_delete:
        return True


parser = argparse.ArgumentParser()
parser.add_argument('filename')
parser.add_argument('-d',
                    '--delete',
                    type=int,
                    nargs='+',
                    help='delete nodes selected by numerical index'
                    )
parser.add_argument('-u',
                    '--update',
                    type=int,
                    nargs='+',
                    help='update nodes selected by numerical index'
                    )
parser.add_argument('-n',
                    '--noprint',
                    help='Supress default printing of an enumerated list of nodes; useful in a pipeline',
                    action='store_true')
args = parser.parse_args()

# Inputs state
source = args.filename
should_print = True #Default
if args.noprint:
    should_print = False
if args.delete:
    nodes_to_delete = [(lambda x: x - 1)(x) for x in args.delete]
    print("Indices of nodes to delete are: " + str(list(nodes_to_delete)))
    #print(str(list(nodes_to_delete)))
else:
    pass
if args.update:
    nodes_to_update = [lambda x: x - 1 for x in args.update]
else:
    pass

# Check inputs
if stdin_is_piped():
    pipe_input = sys.stdin.read()
else: 
   cache = shelve.open('.toc_cache')

   try:
       pipe_input = cache[source]
       print("No input received on stdin; loading from cache")
       cache.close()
   except KeyError:
       cache.close()
       print("no toc for the specified file is found in the cache.")
       sys.exit()

# Program state
if isinstance(pipe_input, str):
    json_representation = json.loads(str(pipe_input))
elif isinstance(pipe_input, dict):
    json_representation = pipe_input
bookmarks = json_representation['bookmarks']

## Apply transformations ##

# Print first, unless supressed
if should_print:
    legibly_print(bookmarks)

# Delete nodes
if args.delete:
    deletion_range = list(range(len(bookmarks)))
    print("deletion range is " + str(deletion_range))
    valid_deletions = filter(lambda x: nodes_to_delete.index(x) not in deletion_range , nodes_to_delete)
    new_bookmarks = filter(lambda x: bookmarks.index(x) not in nodes_to_delete , bookmarks)
    pprint(list(new_bookmarks))
# bookmarks = list(filter(keep_node, bookmarks))

# Update nodes
# TODO: implement update logic



