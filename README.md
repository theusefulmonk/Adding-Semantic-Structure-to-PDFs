# Adding Semantic Structure to PDFs Using Command Line Tools

## About

A workflow demonstration given at International Congress for Medieval Studies, May 16, 2026 in Kalamazoo, Michigan. This was an online session.

(This repository has been made public in advance of the live event, so you may be viewing it before I've actually given the talk.)

## Purpose and Use Case

To understand the purpose and use-case of the talk, please consult the paper available as Adding-Semantic-Structure-to-PDFs.md or Adding-Semantic-Structure-to-PDFs.pdf. This README offers instructions for

1. cloning this repository to your local machine for testing
2. installing tools
3. finding additional resources for learning and experimentation

## Structure of the Repository

```
.
├── Adding-Semantic-Structure-to-PDFs.md
├── Adding-Semantic-Structure-to-PDFs.tex
├── build
│   ├── Adding-Semantic-Structure-to-PDFs.pdf
├── corpus
├── LICENSE.md
├── Makefile
├── README.md
├── requirements.txt
├── sources
├── structure.bib
├── tcApply.sh
├── tcedit
├── tcgen
└── unfinished.json
```

Code examples are in the files examples.md and examples-handout.pdf.

The corpus directory is intended as a convenient place in which to put newly structured pdfs.

The sources directory is a convenient place to put the pdf files to which you will add a document outline.

The build directory holds the results of the build recipes in the Makefile. These are used to generate the final version of the paper and the examples. End users testing the workflow will not ordinarily need to invoke them, but those who wish to learn about Makefiles may find it useful to take a peek.

## Dependencies

- python 3.11
- docling 2.65
- pdfcpu 0.11.1

## Recommendations for Using the Code

This repository is a proof-of-concept. It does not offer a fully-fledged python package. A `requirements.txt` file is provided for users who, after cloning this repo, wish to install a python virtual environment easily to run the scripts it contains. Assuming python 3.11 is already installed on your system, and is available in your PATH, start by creating a python 3.11 virtual environment:

```
# Confirm that your current python is 3.11:
python --version
# Should output something like:
# Python 3.11.*
```

It is likely that the code in this repository will work with later python versions, but it has been tested only with 3.11.

```
git clone blah
cd blah
python -m venv .venv 
```

Then, activate the new virtual environment:

```
source ./.venv/bin/activate
```

Finally, install the required dependencies:

```
pip install -r requirements.txt
```

The final step of applying the table of contents to the pdf relies on `pdfcpu`.
Install it using the appropriate instructions for your platform, as indicated here:

https://pdfcpu.io/getting_started/install_cli/?src=docs

## Current Limitations

At the time this tutorial was given, Docling itself does not seem to be able reliably to produce a nested table of contents, given a book-like pdf input. This could be remedied by giving the provided script `tcedit` the ability to indent a given bookmark so as to produce a nested table of contents structure. Implementing this feature would make an excellent next step for anyone interested in hacking on the script for their own purposes. 

## Additional Resources

You are encouraged to consult the bibliography for the paper, which is also available in this repository. If you are interested in making your pdfs more useful for research purposes, you may want to look at the author's previous paper on efficient vocabulary discovery in pdf documents.

[Vocabulary-Discovery-in-Late-Antique-Texts](https://github.com/theusefulmonk/Vocabulary-Discovery-in-Late-Antique-Texts)
