#!/usr/bin/env python

# Converts an RDF file to tag/value format.
# Usage: rdf_to_tv <rdffile> <tagvaluefile>

if __name__ == '__main__':
    import sys
    import codecs
    from spdx.parsers.rdf import Parser
    from spdx.parsers.loggers import StandardLogger
    from spdx.parsers.rdfbuilders import Builder
    from spdx.writers.tagvalue import write_document, InvalidDocumentError
    infile_name = sys.argv[1]
    outfile_name = sys.argv[2]
    rdfparser = Parser(Builder(), StandardLogger())
    with open(infile_name) as infile:
        document, error = rdfparser.parse(infile)
        if not error:
            # print map(lambda c: c.name, document.creation_info.creators)
            print 'Parsing Successful'
            with codecs.open(outfile_name, mode='w', encoding='utf-8') as outfile:
                try:
                    write_document(document, outfile)
                except InvalidDocumentError:
                    # Note document is valid if error is False
                    print 'Document is Invalid'
        else:
            print 'Errors encountered while parsing RDF file.'
            messages = []
            document.validate(messages)
            print '\n'.join(messages)
