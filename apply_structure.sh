#!/usr/bin/env sh

# Check to see if pdfcpu is installed
if ! which -s pdfcpu; then
    echo "I can't find pdfcpu in your PATH. Please make sure it is installed."
fi

#TODO: check for positional parameter
# Turns out that's a hard problem to solve, so I'm not going to try
# for now.

# pdfcpu requires the json as a file argument, so the following does not currently work.
# Get the json from stdin:
# read json_input 

pdf_input=$1
# pdf_input="./sources/Pseudo-Dionysius_Areopagita_1991_416.pdf"

# Workaround because pdfcpu does not yet accept stdin
cat /dev/fd/0 > .tmp.json #should usually work in Linux and MacOS
json_input=".tmp.json"

pdfcpu bookmarks import $pdf_input $json_input output.pdf 

# Cleanup
# if [ -e ./.tmp.json ] 
# then
#     rm ./.tmp.json
# fi
