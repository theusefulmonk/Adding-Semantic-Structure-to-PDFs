#!/usr/bin/env python3

################################################################################
# Ingest a pdf file containing text with a logical structure and generate json #
# representation of its table of contents in a form that can be consumed by    #
# pdfcpu                                                                       #
################################################################################

from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.backend.docling_parse_backend import DoclingParseDocumentBackend
from docling.backend.docling_parse_v2_backend import DoclingParseV2DocumentBackend
from docling.backend.docling_parse_v4_backend import DoclingParseV4DocumentBackend
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
                backend=DoclingParseV2DocumentBackend,
                pipeline_options=pipeline_options
                )
            }
        )

def mk_toc_item(docling_text_object):
    '''Take an individual docling text object in a texts array and return a
    dictionary in the format needed by pdfcpu'''
    title = docling_text_object['text']
    page = docling_text_object['prov'][0]['page_no']
    toc_item = {'title': title, 'page': page}
    return toc_item

def mk_toc(texts_array):
    '''Take the texts array from the root of a docling json object and return a
    a toc as dictionary in the format needed by pdfcpu'''
    entry_list = [mk_toc_item(i) for i in texts_array if i['label'] == 'section_header']
    toc = {"bookmarks": entry_list}
    return toc

def main():
    # intermediate representation produced by Docling:
    docling_result = converter.convert(source)

    # json output from intermediate representation:
    json_representation = docling_result.document.export_to_dict()

    # the texts array:
    document_texts = json_representation['texts']

    # the toc derived from the texts array:
    document_toc = mk_toc(document_texts)

    # And now print it to stdout
    print(json.dumps(document_toc))
    # print(json.dumps(docling_document.document.export_to_dict()))

if __name__ == "__main__":
    main()
