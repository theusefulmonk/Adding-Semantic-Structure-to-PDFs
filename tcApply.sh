#!/usr/bin/env sh

# Check to see if pdfcpu is installed
if ! which -s pdfcpu; then
    echo "I can't find pdfcpu in your PATH. Please make sure it is installed."
fi

pdf_input=$1

# Workaround because pdfcpu does not yet accept stdin
cat /dev/fd/0 > .tmp.json #should usually work in Linux and MacOS
json_input=".tmp.json"

pdfcpu bookmarks import $pdf_input $json_input output.pdf 

# Cleanup
if [ -e ./.tmp.json ] 
then
    rm ./.tmp.json
fi
