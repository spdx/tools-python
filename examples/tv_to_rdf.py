#!/usr/bin/env python

"""
Converts an tag/value file to RDF format.
Usage: tv_to_rdf <tagvaluefile> <rdffile>
"""
import sys
import codecs
from spdx.parsers.tagvalue import Parser
from spdx.parsers.loggers import StandardLogger
from spdx.parsers.tagvaluebuilders import Builder
from spdx.writers.rdf import write_document, InvalidDocumentError

def convert(infile_name, outfile_name):
    tagvalueparser = Parser(Builder(), StandardLogger())
    tagvalueparser.build()
    with open(infile_name) as infile:
        data = infile.read()
        document, error = tagvalueparser.parse(data)
        if not error:
            # print map(lambda c: c.name, document.creation_info.creators)
            print 'Parsing Successful'
            with open(outfile_name, mode='w') as out:
                write_document(document,out,validate = True)
        else:
            print 'Errors encountered while parsing tag value file.'
            messages = []
            document.validate(messages)
            print '\n'.join(messages)


if __name__ == '__main__':
    infile_name = sys.argv[1]
    outfile_name = sys.argv[2]
    convert(infile_name, outfile_name)