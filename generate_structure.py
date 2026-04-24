#!/usr/bin/env python3

###############
# Ingest a pdf file containing text with a logical structure and generate json
# representation of its table of contents in a form that can be consumed by
# pdfcpu
#######

from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import ThreadedPdfPipelineOptions
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()

source = args.filename

pipeline_options = ThreadedPdfPipelineOptions(
        do_ocr=False,
        do_table_structure=False,
        do_code_enrichment=False,
        do_formula_enrichment=False,
        )

converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options
                )
            }
        )
result = converter.convert(source)

print(json.dumps(result.document.export_to_dict()))
