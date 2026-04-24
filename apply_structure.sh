#!/usr/bin/env sh

# Check to see if pdfcpu is installed
if ! which -s pdfcpu; then
    echo "I can't find pdfcpu in your PATH. Please make sure it is installed."
fi

#TODO: check for positional parameter
# Turns out that's a hard problem to solve, so I'm not going to try
# for now.

# Turns out that passing unicode strings via a unix pipe is fraught.

# Get the json from stdin
#read json_input 

pdf_input=$1

pdfcpu bookmarks import $pdf_input tmp.json output.pdf && rm tmp.json
