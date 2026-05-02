# Structuring Scanned PDFs

## About

## Dependencies

- python 3.11
- docling 2.65
- pdfcpu 0.11.1

## Recommendations for Using the Code

This repository is a proof-of-concept. It does not offer a fully-fledged python
package. A `requirements.txt` file is provided for users who, after cloning
this repo, wish to install a python virtual environment easily to run the
scripts it contains. Assuming python 3.11 is already installed on your system,
and is available in your PATH, start by creating a python 3.11 virtual environment:

```
# Confirm that your current python is 3.11:
python --version
# Should output something like:
# Python 3.11.*
```

It is likely that the code in this repository will work with later python
versions, but it has been tested only with 3.11.

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
