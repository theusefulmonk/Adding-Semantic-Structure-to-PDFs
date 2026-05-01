#!/usr/bin/env python

# This script will provide the ability to edit in the nodes of a pdf table of
# contents in json formt.
# It is designed for optional use in a shell pipeline
# But can be invoked with a filename argument to look up a previously generated
# toc in the cache

import sys
import os
import stat
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

# borrowed from here: 
# https://gist.github.com/fralau/061a4f6c13251367ef1d9a9a99fb3e8d
def parse_var(s):
    """
    Parse a key, value pair, separated by '='
    That's the reverse of ShellArgs.

    On the command line (argparse) a declaration will typically look like:
        foo=hello
    or
        foo="hello world"
    """
    items = s.split('=')
    key = items[0].strip() # we remove blanks around keys, as is logical
    if len(items) > 1:
        # rejoin the rest:
        value = '='.join(items[1:])
    return (key, value)


def parse_vars(items):
    """
    Parse a series of key-value pairs and return a dictionary
    """
    d = {}

    if items:
        for item in items:
            key, value = parse_var(item)
            d[key] = value
    return d

def update_nodes(dictionary_of_nodes, bookmarks):
    """
    Update nodes based on dictionary of nodes to update and a list of bookmark
    nodes. Return a new bookmark list.
    """
    OFFSET = -1
    for k,v in dictionary_of_nodes.items():
        node_contents = v.split(",", 1) # result is a list
        node_type = node_contents[0]
        node_value = node_contents[1]
        #wrapped = f'{{"{node_value}"}}'
        bookmarks[int(k) + OFFSET][node_type] = node_value
    return bookmarks

parser = argparse.ArgumentParser()
parser.add_argument('filename',
                    type=str,
                    #type=argparse.FileType('r'),
                    nargs='?',
                    default='-'
                    )
parser.add_argument('-d',
                    '--delete',
                    type=int,
                    nargs='+',
                    help='delete nodes selected by numerical index'
                    )
parser.add_argument('-u',
                    '--update',
                    metavar="KEY=VALUE",
                    nargs='+',
                    help='update nodes selected by numerical index'
                    )
parser.add_argument('-n',
                    '--noprint',
                    help='Supress default printing of an enumerated list of nodes; useful in a pipeline',
                    action='store_true')
parser.add_argument('-f',
                    '--final',
                    help='Output final version formatted for pdf cpu. Call last in the pipeline.',
                    action='store_true')
args = parser.parse_args()

# Check inputs
if stdin_is_piped():
    #print("INFO: The tweak script is reading from stdin.")
    program_input = sys.stdin.read()
    #print(program_input)
    #with standard_input:
    #    pipe_input = standard_input.read()
else: 
    # The script has been invoked standalone, not in a pipeline.
   cache = shelve.open('.toc_cache')
   try:
       # Convert to string so we don't have to worry about how program_input was loaded
       program_input = json.dumps(cache[args.filename], ensure_ascii=False)
       print("INFO: No input received on stdin; loading from cache.")
       #print(program_input)
       cache.close()
   except KeyError:
       cache.close()
       print("ERROR: No toc for the specified file is found in the cache.")
       sys.exit()
# Flags state
should_print = True # Default
if args.noprint:
    should_print = False
if args.delete:
    should_print = False
    nodes_to_delete = [(lambda x: x - 1)(x) for x in args.delete]
if args.update:
    should_print = False
    nodes_to_update = parse_vars(args.update)
if args.final:
    should_print = False


# Program state
#if isinstance(program_input, str):
#    #print("piped input is " + program_input)
#    json_representation = json.loads(program_input)
#    print("loaded from standard input.")
#elif isinstance(program_input, dict):
#    json_representation = program_input
#    print("No filename given. Loaded from cache")
json_representation = json.loads(program_input)
if 'bookmarks' in json_representation:
    bookmarks = json_representation['bookmarks']
else: # We already have a bookmark list
    bookmarks = json_representation


## Apply transformations ##

# Print first, unless supressed
if should_print:
    print((
        'When invoked without options, this program prints a visual representation of the bookmark tree and then exits without applying any transformation. '
        'When you are ready to transform the bookmark tree, specify the -d(elete) or -u(pdate) flags, followed by the index numbers of nodes you wish to modify. ' 
        'Doing this will suppress printing the visual representation and will instead print the raw output tree to standard output for use by another program. '
        '\n'
        ))
    legibly_print(bookmarks)
    # If we are simply legibly printing to see what we want to modify
    # there is no need to output further in the pipeline.
    sys.exit()


# Update nodes
# syntax: 1=k,v (that is, node 1 should be set to this key,value pair)
if args.update:
   bookmarks = update_nodes(nodes_to_update, bookmarks)

# Delete nodes
if args.delete:
    # Invalid and repeated nodes are automatically ignored
    bookmarks = list(filter(lambda x: bookmarks.index(x) not in nodes_to_delete, bookmarks))

# TODO: implement a convenient range syntax: e.g., 1-5
# probably needs to be handled in the argument parsing logic.
# Indent nodes
# TODO: implement indentation logic

# Prepare for pdfcpu
# expects a toplevel "bookmarks" key.
bookmarks_tree = {"bookmarks": bookmarks}

# Finally, output new node structure to sdout
# optionally prepare it for pdfcpu
if args.final:
    print(json.dumps(bookmarks_tree, ensure_ascii=False))
else:
    print(json.dumps(bookmarks, ensure_ascii=False))



