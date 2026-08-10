# Adding Semantic Structure to PDFs Using Command Line Tools

## About

A workflow demonstration given at International Congress for Medieval Studies, May 16, 2026 in Kalamazoo, Michigan. This was an online session. 

The workflow itself is pitched at an intermediate level. It presumes some familiarity with working at the command line and with the python ecosystem, as well as some basic programming concepts. But if you are a beginner interested in seeing how python might help you do useful things for your work, you are most welcome. If you need a practical, beginner-friendly introduction to Python, I highly recommend Al Sweigart's [*Automate the Boring Stuff with Python*](https://automatetheboringstuff.com).

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

The corpus directory is intended as a convenient place in which to put newly structured pdfs.

The sources directory is a convenient place to put the pdf files to which you will add a document outline.

The build directory holds the results of the build recipes in the Makefile. These are used to generate the final version of the paper and the examples. End users testing the workflow will not ordinarily need to invoke them, but those who wish to learn about Makefiles may find it useful to take a peek.

## Dependencies

- python 3.11 or greater
- [docling 2.65](https://docling-project.github.io/docling/) or greater
- [pdfcpu 0.11.1](https://pdfcpu.io) or greater

## Recommendations for Using the Code

This repository is a proof-of-concept. It does not offer a fully-fledged python package. The recommended approach to using this code is to clone the repository and then create a virtual environment into which you will install docling. You should be able to use any python version ≥ 3.11.

First, clone the repository and set up the virtual environment inside it.

```
git clone https://github.com/theusefulmonk/Adding-Semantic-Structure-to-PDFs.git
cd Adding-Semantic-Structure-to-PDFs
python -m venv .venv 
```

Then, activate the new virtual environment:

```
source ./.venv/bin/activate
```

Your shell prompt will likely change to indicate that the virtual environment is active. You can check by issuing the command `which python` which should return the path to the python interpreter in the virtual environment directory (`.venv`, if you've been following this example). Finally, install the required dependencies:

```
python -m pip install docling==2.65.0
```

The final step of applying the table of contents to the pdf relies on `pdfcpu`.
Install it using the appropriate instructions for your platform, as indicated here:

https://pdfcpu.io/getting_started/install_cli/?src=docs

One note of caution: depending on your distribution of Linux, `pdfcpu` may be out of date in your distribution's package manager. You need a version ≥ 0.11.1. You may need to install it manually. But you may find it more convenient to use [`homebrew`](https://brew.sh).

If you want to try to recreate the environment used in this demonstration exactly, you have two options: (1) use the provided `requirements.txt` or (2) use the provided nix flake. 

### Using `Requirements.txt`

Ensure that you are running python 3.11 and using same platform and architecture (MacOS and Apple Silicon) as was used in the demonstration.  

Assuming python 3.11 is already
installed on your system, and is available in your PATH, start by creating a
python 3.11 virtual environment:

```
# Confirm that your current python is 3.11:
python --version
# Should output something like:
# Python 3.11.*
```
Then, clone the repository and set up a virtual environment as before. With the
environment activated, you can then call

```
pip install -r requirements.txt
```

### Using Nix

Note: Nix is the best way to ensure a reproducible environment, but using it is probably most suited to more advanced users. Assuming you have the nix package manager installed, then within the directory

```
nix develop

# Or, if you are using direnv, you can take advantage of the provided .envrc

direnv allow
```

Either approach will automatically set up your environment with the precise versions of python, docling, and pdfcpu you need to run the scripts.

## Current Limitations

At the time this demonstration was given, Docling itself does not seem to be able reliably to produce a nested table of contents, given a book-like pdf input. This could be remedied by giving the provided script `tcedit` the ability to indent a given bookmark so as to produce a nested table of contents structure. Implementing this feature would make an excellent next step for anyone interested in hacking on the script for their own purposes. 

## Additional Resources

You are encouraged to consult the bibliography for the paper, which is also available in this repository. If you are interested in making your pdfs more useful for research purposes, you may want to look at the author's previous paper on efficient vocabulary discovery in pdf documents.

[Vocabulary-Discovery-in-Late-Antique-Texts](https://github.com/theusefulmonk/Vocabulary-Discovery-in-Late-Antique-Texts)
